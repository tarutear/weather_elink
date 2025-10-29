"""
E-ink 하드웨어 디스플레이 제어 모듈
Waveshare E-Paper HAT 지원
"""

try:
    from waveshare_epd import epd7in5_V2  # 7.5inch V2
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False

from PIL import Image
import time


class HardwareDisplay:
    """Waveshare E-Paper HAT 제어 클래스"""

    def __init__(self, model: str = "7in5_V2"):
        """
        HardwareDisplay 초기화

        Args:
            model: E-Paper 모델 (예: "7in5_V2", "4in2", "2in9_V2")
        """
        if not HARDWARE_AVAILABLE:
            raise ImportError(
                "Waveshare EPD 라이브러리가 필요합니다.\n"
                "설치: pip install waveshare-epd\n"
                "또는: https://github.com/waveshare/e-Paper"
            )

        self.model = model
        self.epd = None
        self._load_driver(model)

    def _load_driver(self, model: str):
        """모델에 맞는 드라이버 로드"""
        try:
            if model == "7in5_V2":
                from waveshare_epd import epd7in5_V2
                self.epd = epd7in5_V2.EPD()
            elif model == "4in2":
                from waveshare_epd import epd4in2
                self.epd = epd4in2.EPD()
            elif model == "2in9_V2":
                from waveshare_epd import epd2in9_V2
                self.epd = epd2in9_V2.EPD()
            else:
                raise ValueError(f"지원하지 않는 모델: {model}")

        except ImportError as e:
            raise ImportError(f"모델 '{model}' 드라이버를 찾을 수 없습니다: {e}")

    def init(self):
        """디스플레이 초기화"""
        print(f"🔌 E-ink 디스플레이 ({self.model}) 초기화 중...")
        try:
            self.epd.init()
            print("✅ 초기화 완료!")
        except Exception as e:
            print(f"❌ 초기화 실패: {e}")
            raise

    def clear(self):
        """디스플레이 지우기"""
        print("🧹 디스플레이 클리어 중...")
        try:
            self.epd.Clear()
            print("✅ 클리어 완료!")
        except Exception as e:
            print(f"❌ 클리어 실패: {e}")

    def display_image(self, image_path: str):
        """
        이미지를 디스플레이에 표시

        Args:
            image_path: 표시할 이미지 파일 경로
        """
        print(f"📺 디스플레이 업데이트 중: {image_path}")
        start_time = time.time()

        try:
            # 이미지 로드
            image = Image.open(image_path)

            # 해상도 확인
            epd_width = self.epd.width
            epd_height = self.epd.height

            if image.size != (epd_width, epd_height):
                print(f"⚠️  이미지 크기 조정: {image.size} → ({epd_width}, {epd_height})")
                image = image.resize((epd_width, epd_height), Image.Resampling.LANCZOS)

            # 디스플레이에 표시
            self.epd.display(self.epd.getbuffer(image))

            elapsed = time.time() - start_time
            print(f"✅ 디스플레이 업데이트 완료! (소요시간: {elapsed:.1f}초)")

        except FileNotFoundError:
            print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        except Exception as e:
            print(f"❌ 디스플레이 업데이트 실패: {e}")
            raise

    def sleep(self):
        """디스플레이 절전 모드 (배터리 절약)"""
        print("💤 디스플레이 절전 모드...")
        try:
            self.epd.sleep()
        except Exception as e:
            print(f"⚠️  절전 모드 실패: {e}")


def test_hardware_display():
    """하드웨어 디스플레이 테스트"""
    import os

    if not HARDWARE_AVAILABLE:
        print("❌ 하드웨어 라이브러리가 설치되지 않았습니다.")
        print("\n설치 방법:")
        print("  pip install waveshare-epd")
        print("\n또는:")
        print("  git clone https://github.com/waveshare/e-Paper.git")
        print("  cd e-Paper/RaspberryPi_JetsonNano/python")
        print("  sudo python setup.py install")
        return

    # 테스트 이미지 찾기
    test_images = [
        "output/weather_test.png",
        "output/weather_*.png",
    ]

    image_path = None
    for pattern in test_images:
        import glob
        matches = glob.glob(pattern)
        if matches:
            image_path = matches[0]
            break

    if not image_path:
        print("❌ 테스트할 이미지가 없습니다.")
        print("먼저 'python main.py'를 실행하여 이미지를 생성하세요.")
        return

    # 하드웨어 디스플레이 테스트
    try:
        display = HardwareDisplay(model="7in5_V2")
        display.init()
        display.clear()
        display.display_image(image_path)
        display.sleep()

        print("\n✅ 하드웨어 디스플레이 테스트 완료!")

    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_hardware_display()
