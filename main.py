#!/usr/bin/env python3
"""
Weather E-ink Dashboard
E-ink 디스플레이를 위한 날씨 대시보드 메인 프로그램
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import yaml

from src.weather_api import WeatherAPI
from src.display_generator import DisplayGenerator
from src.scheduler import WeatherScheduler


class WeatherDashboard:
    """날씨 대시보드 메인 클래스"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        WeatherDashboard 초기화

        Args:
            config_path: 설정 파일 경로
        """
        # .env 파일 로드
        load_dotenv()

        # 설정 파일 로드
        self.config = self._load_config(config_path)

        # API 키 확인
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            print("❌ 오류: OPENWEATHER_API_KEY가 설정되지 않았습니다.")
            print("\n.env 파일을 생성하고 다음을 추가하세요:")
            print("OPENWEATHER_API_KEY=your_api_key_here")
            print("\nAPI 키는 https://openweathermap.org/api 에서 무료로 발급받을 수 있습니다.")
            sys.exit(1)

        # Weather API 초기화
        self.weather_api = WeatherAPI(
            api_key=self.api_key,
            city=self.config["location"]["city"],
            country=self.config["location"]["country"]
        )

        # Display Generator 초기화
        self.display_generator = DisplayGenerator(
            width=self.config["display"]["width"],
            height=self.config["display"]["height"],
            color_mode=self.config["display"]["color_mode"]
        )

        # 출력 디렉토리 생성
        self.output_dir = Path(self.config["output"]["directory"])
        self.output_dir.mkdir(exist_ok=True)

    def _load_config(self, config_path: str) -> dict:
        """설정 파일 로드"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ 설정 파일 파싱 오류: {e}")
            sys.exit(1)

    def update_weather(self):
        """날씨 정보 업데이트 및 이미지 생성"""
        try:
            # 날씨 정보 가져오기
            print("🌡  현재 날씨 정보 가져오는 중...")
            current = self.weather_api.get_current_weather(
                lat=self.config["location"]["latitude"],
                lon=self.config["location"]["longitude"]
            )

            if not current:
                print("❌ 현재 날씨 정보를 가져올 수 없습니다.")
                return

            print(f"   {current['location']}: {current['temperature']}°C, {current['weather_description']}")

            # 예보 정보 가져오기
            print("📊 예보 정보 가져오는 중...")
            forecast = self.weather_api.get_forecast(
                lat=self.config["location"]["latitude"],
                lon=self.config["location"]["longitude"],
                hours=self.config["ui"]["forecast_hours"]
            )

            print(f"   {len(forecast)}개 예보 데이터 수신")

            # 일별 예보 가져오기
            print("📅 7일 예보 정보 가져오는 중...")
            daily_forecast = self.weather_api.get_daily_forecast(
                lat=self.config["location"]["latitude"],
                lon=self.config["location"]["longitude"],
                days=7
            )

            print(f"   {len(daily_forecast)}일 예보 데이터 수신")

            # 이미지 생성
            print("🖼  E-ink 디스플레이 이미지 생성 중...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.config["output"]["filename_pattern"].replace("{timestamp}", timestamp)
            filepath = self.output_dir / filename

            # PIL 렌더러 사용 (InkyPi 스타일 디자인)
            self.display_generator.generate_weather_display(current, forecast, daily_forecast)
            self.display_generator.save(str(filepath))

            # 이전 파일 정리 (옵션)
            if self.config["output"]["keep_history"]:
                self._cleanup_old_files()

            print(f"✅ 완료! 이미지 저장됨: {filepath}")

            # 디스플레이 모드 확인
            if self.config["display"]["mode"] == "hardware":
                self._update_hardware_display(str(filepath))

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()

    def _cleanup_old_files(self):
        """오래된 이미지 파일 정리"""
        max_files = self.config["output"]["max_history_files"]
        files = sorted(self.output_dir.glob("weather_*.png"))

        if len(files) > max_files:
            for file in files[:-max_files]:
                file.unlink()
                print(f"🗑  오래된 파일 삭제: {file.name}")

    def _update_hardware_display(self, filepath: str):
        """하드웨어 디스플레이 업데이트"""
        print("\n🔌 하드웨어 디스플레이 업데이트...")

        try:
            display_type = self.config["display"].get("display_type", "waveshare")

            if display_type == "inky":
                # Pimoroni Inky Impression (7색)
                print("   디스플레이: Pimoroni Inky Impression")
                from src.inky_display import InkyDisplay
                display = InkyDisplay()
                display.display_image(filepath)

            else:
                # Waveshare E-Paper
                print(f"   디스플레이: Waveshare E-Paper")
                from src.hardware_display import HardwareDisplay
                model = self.config["display"].get("epaper_model", "7in5_V2")
                display = HardwareDisplay(model=model)
                display.init()
                display.display_image(filepath)
                display.sleep()

            print("✅ 하드웨어 디스플레이 업데이트 완료!\n")

        except ImportError as e:
            print(f"⚠️  하드웨어 모드 오류: {e}")
            print("\n해결 방법:")
            print("  Inky: pip install inky[rpi,fonts]")
            print("  Waveshare: pip install waveshare-epd")
            print("  또는 config.yaml에서 mode를 'simulation'으로 변경")
            print("  자세한 설치 방법은 INKY_SETUP_GUIDE.md 또는 HARDWARE_SETUP.md 참고\n")

        except Exception as e:
            print(f"❌ 디스플레이 업데이트 실패: {e}")
            import traceback
            traceback.print_exc()

    def run_once(self):
        """한 번만 실행"""
        print("\n" + "=" * 60)
        print("🌤  날씨 E-ink 대시보드")
        print("=" * 60 + "\n")

        self.update_weather()

        print("\n" + "=" * 60)

    def run_scheduled(self):
        """스케줄러로 실행"""
        interval = self.config["weather_api"]["update_interval"]
        scheduler = WeatherScheduler(self.update_weather, interval_seconds=interval)
        scheduler.start(run_immediately=True)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="Weather E-ink Dashboard - E-ink 디스플레이용 날씨 대시보드"
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="백그라운드에서 자동 업데이트 (기본값: 한 번만 실행)"
    )
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="설정 파일 경로 (기본값: config/config.yaml)"
    )

    args = parser.parse_args()

    # 대시보드 실행
    dashboard = WeatherDashboard(config_path=args.config)

    if args.daemon:
        # 스케줄러 모드
        dashboard.run_scheduled()
    else:
        # 한 번만 실행
        dashboard.run_once()


if __name__ == "__main__":
    main()
