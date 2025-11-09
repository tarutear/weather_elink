"""
Pimoroni Inky Impression 디스플레이 제어 모듈
7색 E-ink 디스플레이 지원
"""

try:
    from inky.auto import auto
    from inky import Inky7Colour
    INKY_AVAILABLE = True
except ImportError:
    INKY_AVAILABLE = False

from PIL import Image
import time


class InkyDisplay:
    """Pimoroni Inky Impression 제어 클래스"""

    def __init__(self):
        """InkyDisplay 초기화"""
        if not INKY_AVAILABLE:
            raise ImportError(
                "Inky 라이브러리가 필요합니다.\n"
                "설치: pip install inky[rpi,fonts]"
            )

        # Inky 디스플레이 자동 감지
        try:
            self.inky = auto(ask_user=False, verbose=True)
            print(f"✅ Inky 디스플레이 감지: {type(self.inky).__name__}")
            print(f"   해상도: {self.inky.width}x{self.inky.height}")
            print(f"   색상: {self.inky.colour}")
        except Exception as e:
            print(f"⚠️  자동 감지 실패, 수동으로 Inky Impression 7.3\" 설정")
            self.inky = Inky7Colour()

    def display_image(self, image_path: str):
        """
        이미지를 디스플레이에 표시

        Args:
            image_path: 표시할 이미지 파일 경로
        """
        print(f"\n📺 Inky Impression 디스플레이 업데이트 중...")
        print(f"   이미지: {image_path}")
        start_time = time.time()

        try:
            # 이미지 로드
            image = Image.open(image_path)

            # 해상도 확인 및 조정
            if image.size != (self.inky.width, self.inky.height):
                print(f"   이미지 크기 조정: {image.size} → ({self.inky.width}, {self.inky.height})")
                image = image.resize((self.inky.width, self.inky.height), Image.Resampling.LANCZOS)

            # 7색 팔레트로 변환
            # Inky Impression은 자동으로 최적의 7색으로 변환
            print("   🎨 7색 팔레트로 변환 중...")

            # 이미지 설정
            self.inky.set_image(image)

            # 디스플레이 업데이트 (시간이 걸립니다!)
            print("   ⏳ 디스플레이 업데이트 중... (약 30초 소요)")
            self.inky.show()

            elapsed = time.time() - start_time
            print(f"✅ 디스플레이 업데이트 완료! (소요시간: {elapsed:.1f}초)\n")

        except FileNotFoundError:
            print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
            raise
        except Exception as e:
            print(f"❌ 디스플레이 업데이트 실패: {e}")
            raise


def test_inky_display():
    """Inky 디스플레이 테스트"""
    import os
    import glob

    if not INKY_AVAILABLE:
        print("❌ Inky 라이브러리가 설치되지 않았습니다.")
        print("\n설치 방법:")
        print("  pip install inky[rpi,fonts]")
        return

    # 테스트 이미지 찾기
    test_images = glob.glob("output/weather_*.png")

    if not test_images:
        print("❌ 테스트할 이미지가 없습니다.")
        print("먼저 'python main.py'를 실행하여 이미지를 생성하세요.")
        return

    image_path = test_images[0]
    print(f"테스트 이미지: {image_path}")

    # Inky 디스플레이 테스트
    try:
        display = InkyDisplay()
        display.display_image(image_path)
        print("\n✅ Inky 디스플레이 테스트 완료!")
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_inky_display()
