"""
E-ink 디스플레이용 이미지 생성 모듈
날씨 정보를 E-ink 디스플레이에 최적화된 이미지로 변환합니다.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from typing import Dict, List, Tuple
import os


class DisplayGenerator:
    """E-ink 디스플레이 이미지 생성기"""

    # E-ink 디스플레이 색상 (흑백)
    COLOR_BLACK = 0
    COLOR_WHITE = 255
    COLOR_RED = 128  # 3색 디스플레이용

    # 날씨 아이콘 유니코드
    WEATHER_ICONS = {
        "clear": "☀",
        "few_clouds": "🌤",
        "clouds": "☁",
        "rain": "🌧",
        "thunder": "⛈",
        "snow": "🌨",
        "mist": "🌫",
        "unknown": "?",
    }

    def __init__(self, width: int = 800, height: int = 480, color_mode: str = "bw"):
        """
        DisplayGenerator 초기화

        Args:
            width: 디스플레이 너비 (기본값: 800)
            height: 디스플레이 높이 (기본값: 480)
            color_mode: 색상 모드 ('bw', 'bwr', '7color')
        """
        self.width = width
        self.height = height
        self.color_mode = color_mode

        # 이미지 생성 (흑백)
        if color_mode == "bw":
            self.image = Image.new("L", (width, height), self.COLOR_WHITE)
        else:
            self.image = Image.new("RGB", (width, height), (255, 255, 255))

        self.draw = ImageDraw.Draw(self.image)

        # 폰트 로드 (시스템 폰트 사용)
        self._load_fonts()

    def _load_fonts(self):
        """시스템 폰트 로드"""
        try:
            # 한글 지원 폰트 경로 (Ubuntu/Debian 기준)
            font_paths = [
                "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
                "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
            ]

            font_path = None
            for path in font_paths:
                if os.path.exists(path):
                    font_path = path
                    break

            if font_path:
                self.font_large = ImageFont.truetype(font_path, 72)
                self.font_medium = ImageFont.truetype(font_path, 36)
                self.font_small = ImageFont.truetype(font_path, 24)
                self.font_tiny = ImageFont.truetype(font_path, 18)
            else:
                # 폰트를 찾지 못한 경우 기본 폰트 사용
                print("⚠️  한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
                self.font_large = ImageFont.load_default()
                self.font_medium = ImageFont.load_default()
                self.font_small = ImageFont.load_default()
                self.font_tiny = ImageFont.load_default()

        except Exception as e:
            print(f"폰트 로드 실패: {e}")
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def generate_weather_display(self, current: Dict, forecast: List[Dict]) -> Image:
        """
        날씨 대시보드 이미지 생성

        Args:
            current: 현재 날씨 정보
            forecast: 예보 정보 리스트

        Returns:
            생성된 PIL Image 객체
        """
        if not current:
            self._draw_error_message("날씨 정보를 가져올 수 없습니다.")
            return self.image

        # 배경 그리기
        self._draw_background()

        # 헤더 (날짜/시간, 위치)
        self._draw_header(current)

        # 현재 날씨 (왼쪽 영역)
        self._draw_current_weather(current)

        # 예보 (오른쪽 영역)
        if forecast:
            self._draw_forecast(forecast)

        # 푸터 (추가 정보)
        self._draw_footer(current)

        return self.image

    def _draw_background(self):
        """배경 그리기"""
        # 흰색 배경 (이미 초기화 시 설정됨)
        # 경계선 그리기
        self.draw.rectangle(
            [(0, 0), (self.width - 1, self.height - 1)],
            outline=self.COLOR_BLACK,
            width=2
        )

    def _draw_header(self, current: Dict):
        """헤더 그리기 (날짜/시간, 위치)"""
        # 현재 시간
        now = datetime.now()
        date_str = now.strftime("%Y년 %m월 %d일")
        time_str = now.strftime("%H:%M")

        # 날짜
        self.draw.text(
            (20, 10),
            date_str,
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

        # 시간 (오른쪽 정렬)
        time_bbox = self.draw.textbbox((0, 0), time_str, font=self.font_medium)
        time_width = time_bbox[2] - time_bbox[0]
        self.draw.text(
            (self.width - time_width - 20, 10),
            time_str,
            fill=self.COLOR_BLACK,
            font=self.font_medium
        )

        # 위치
        location = current.get("location", "서울")
        self.draw.text(
            (20, 50),
            f"📍 {location}",
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

        # 구분선
        self.draw.line(
            [(10, 90), (self.width - 10, 90)],
            fill=self.COLOR_BLACK,
            width=2
        )

    def _draw_current_weather(self, current: Dict):
        """현재 날씨 그리기 (왼쪽 영역)"""
        y_offset = 110

        # 온도 (크게)
        temp = f"{current['temperature']}°"
        self.draw.text(
            (30, y_offset),
            temp,
            fill=self.COLOR_BLACK,
            font=self.font_large
        )

        # 날씨 설명
        desc = current.get("weather_description", "")
        self.draw.text(
            (30, y_offset + 90),
            desc,
            fill=self.COLOR_BLACK,
            font=self.font_medium
        )

        # 체감 온도
        feels = f"체감 {current['feels_like']}°"
        self.draw.text(
            (30, y_offset + 140),
            feels,
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

        # 최저/최고 온도
        temp_range = f"↓ {current['temp_min']}°  ↑ {current['temp_max']}°"
        self.draw.text(
            (30, y_offset + 175),
            temp_range,
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

        # 추가 정보
        info_y = y_offset + 220
        info_items = [
            f"💧 습도: {current['humidity']}%",
            f"💨 풍속: {current['wind_speed']} m/s",
            f"🌅 일출: {current['sunrise']}",
            f"🌇 일몰: {current['sunset']}",
        ]

        for i, item in enumerate(info_items):
            self.draw.text(
                (30, info_y + i * 30),
                item,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

    def _draw_forecast(self, forecast: List[Dict]):
        """예보 그리기 (오른쪽 영역)"""
        # 예보 제목
        self.draw.text(
            (self.width // 2 + 20, 110),
            "시간별 예보",
            fill=self.COLOR_BLACK,
            font=self.font_medium
        )

        # 예보 항목
        y_offset = 160
        x_offset = self.width // 2 + 20

        for i, f in enumerate(forecast[:4]):  # 최대 4개 표시
            y_pos = y_offset + i * 70

            # 시간
            time_str = f.get("time", "")
            self.draw.text(
                (x_offset, y_pos),
                time_str,
                fill=self.COLOR_BLACK,
                font=self.font_small
            )

            # 온도
            temp_str = f"{f['temperature']}°"
            self.draw.text(
                (x_offset + 80, y_pos),
                temp_str,
                fill=self.COLOR_BLACK,
                font=self.font_small
            )

            # 날씨
            desc = f.get("weather_description", "")
            self.draw.text(
                (x_offset + 150, y_pos),
                desc,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

            # 강수확률
            pop = f.get("pop", 0)
            if pop > 0:
                pop_str = f"💧 {pop}%"
                self.draw.text(
                    (x_offset, y_pos + 25),
                    pop_str,
                    fill=self.COLOR_BLACK,
                    font=self.font_tiny
                )

    def _draw_footer(self, current: Dict):
        """푸터 그리기"""
        # 구분선
        y = self.height - 40
        self.draw.line(
            [(10, y), (self.width - 10, y)],
            fill=self.COLOR_BLACK,
            width=1
        )

        # 업데이트 시간
        update_time = f"마지막 업데이트: {datetime.now().strftime('%H:%M')}"
        self.draw.text(
            (20, y + 10),
            update_time,
            fill=self.COLOR_BLACK,
            font=self.font_tiny
        )

    def _draw_error_message(self, message: str):
        """에러 메시지 그리기"""
        self.draw.text(
            (self.width // 2 - 100, self.height // 2),
            message,
            fill=self.COLOR_BLACK,
            font=self.font_medium
        )

    def save(self, filepath: str):
        """
        이미지 저장

        Args:
            filepath: 저장할 파일 경로
        """
        # E-ink에 최적화된 형식으로 변환
        if self.color_mode == "bw":
            # 1-bit 흑백으로 변환 (dithering 적용)
            self.image = self.image.convert("1")

        self.image.save(filepath)
        print(f"✅ 이미지 저장됨: {filepath}")

    def show(self):
        """이미지 미리보기 (개발용)"""
        self.image.show()


def test_display_generator():
    """디스플레이 생성기 테스트"""
    # 샘플 데이터
    current = {
        "timestamp": datetime.now().isoformat(),
        "location": "서울",
        "temperature": 15.5,
        "feels_like": 13.2,
        "temp_min": 12.0,
        "temp_max": 18.0,
        "humidity": 65,
        "pressure": 1013,
        "weather_main": "Clear",
        "weather_description": "맑음",
        "weather_icon": "01d",
        "wind_speed": 3.5,
        "wind_deg": 180,
        "clouds": 10,
        "sunrise": "06:30",
        "sunset": "18:45",
    }

    forecast = [
        {
            "time": "15:00",
            "temperature": 16.0,
            "weather_description": "맑음",
            "pop": 0,
        },
        {
            "time": "18:00",
            "temperature": 14.5,
            "weather_description": "구름 조금",
            "pop": 10,
        },
        {
            "time": "21:00",
            "temperature": 12.0,
            "weather_description": "흐림",
            "pop": 30,
        },
        {
            "time": "00:00",
            "temperature": 10.5,
            "weather_description": "비",
            "pop": 70,
        },
    ]

    # 이미지 생성
    generator = DisplayGenerator(width=800, height=480)
    image = generator.generate_weather_display(current, forecast)

    # 저장
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"weather_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(output_dir, filename)
    generator.save(filepath)

    print(f"\n테스트 이미지가 생성되었습니다: {filepath}")
    print("output 폴더를 확인하세요!")


if __name__ == "__main__":
    test_display_generator()
