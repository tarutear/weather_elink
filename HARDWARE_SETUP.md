"""
E-ink 하드웨어 연결 가이드
"""

# ========================================
# Waveshare E-Paper HAT 연결 가이드
# ========================================

## 1. 하드웨어 연결

### Waveshare 7.5inch E-Paper HAT
- Raspberry Pi GPIO 핀에 직접 꽂기만 하면 됨 (HAT 형태)
- 별도 배선 불필요!

### 연결 순서:
1. Raspberry Pi 전원 끄기
2. E-Paper HAT를 GPIO 핀에 조심스럽게 연결
3. 전원 켜기

## 2. 소프트웨어 설정

### 2.1 SPI 활성화
```bash
sudo raspi-config
# Interface Options → SPI → Enable 선택
sudo reboot
```

### 2.2 Waveshare 라이브러리 설치

#### 방법 1: 공식 라이브러리
```bash
# Waveshare 공식 저장소 클론
git clone https://github.com/waveshare/e-Paper.git
cd e-Paper/RaspberryPi_JetsonNano/python

# 라이브러리 설치
sudo python3 setup.py install

# 예제 테스트
cd examples
python3 epd_7in5_V2_test.py
```

#### 방법 2: pip 설치 (더 간단)
```bash
pip3 install waveshare-epd
```

### 2.3 필요한 시스템 패키지
```bash
sudo apt-get update
sudo apt-get install python3-pil python3-numpy
```

## 3. 코드 통합

### 3.1 하드웨어 디스플레이 모듈 추가

`src/hardware_display.py` 파일 생성:

```python
"""
E-ink 하드웨어 디스플레이 제어 모듈
"""

try:
    from waveshare_epd import epd7in5_V2  # 7.5inch V2
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False
    print("⚠️  Waveshare 라이브러리가 설치되지 않았습니다.")

from PIL import Image


class HardwareDisplay:
    """Waveshare E-Paper HAT 제어 클래스"""

    def __init__(self):
        if not HARDWARE_AVAILABLE:
            raise ImportError("Waveshare EPD 라이브러리가 필요합니다.")

        self.epd = epd7in5_V2.EPD()

    def init(self):
        """디스플레이 초기화"""
        print("🔌 E-ink 디스플레이 초기화 중...")
        self.epd.init()
        self.epd.Clear()
        print("✅ 초기화 완료!")

    def display_image(self, image_path: str):
        """이미지를 디스플레이에 표시"""
        print(f"📺 디스플레이 업데이트 중: {image_path}")

        # 이미지 로드
        image = Image.open(image_path)

        # 디스플레이에 표시
        self.epd.display(self.epd.getbuffer(image))
        print("✅ 디스플레이 업데이트 완료!")

    def sleep(self):
        """디스플레이 절전 모드"""
        print("💤 디스플레이 절전 모드...")
        self.epd.sleep()


# 사용 예제
if __name__ == "__main__":
    display = HardwareDisplay()
    display.init()
    display.display_image("output/weather_test.png")
    display.sleep()
```

### 3.2 main.py 수정

`main.py`의 `_update_hardware_display()` 함수를 다음과 같이 수정:

```python
def _update_hardware_display(self, filepath: str):
    """하드웨어 디스플레이 업데이트"""
    try:
        from src.hardware_display import HardwareDisplay

        display = HardwareDisplay()
        display.init()
        display.display_image(filepath)
        display.sleep()

        print("✅ 하드웨어 디스플레이 업데이트 완료!")

    except ImportError as e:
        print(f"⚠️  하드웨어 모드 오류: {e}")
        print("   시뮬레이션 모드로 실행하거나 라이브러리를 설치하세요.")
    except Exception as e:
        print(f"❌ 디스플레이 업데이트 실패: {e}")
```

### 3.3 config.yaml 수정

```yaml
display:
  width: 800
  height: 480
  mode: "hardware"  # simulation → hardware로 변경!
  color_mode: "bw"
```

## 4. 실행

```bash
# 하드웨어 모드로 실행
python3 main.py

# 매시간 자동 업데이트
python3 main.py --daemon
```

## 5. 다른 해상도 제품 사용시

### 4.2inch (400×300)
```python
from waveshare_epd import epd4in2  # 라이브러리만 변경

# config.yaml
display:
  width: 400
  height: 300
```

### 2.9inch (296×128)
```python
from waveshare_epd import epd2in9_V2

# config.yaml
display:
  width: 296
  height: 128
```

## 6. 문제 해결

### SPI 오류
```bash
# SPI가 활성화되어 있는지 확인
ls /dev/spidev*
# /dev/spidev0.0 /dev/spidev0.1 가 보여야 함
```

### 권한 오류
```bash
# 현재 사용자를 spi 그룹에 추가
sudo usermod -a -G spi,gpio $USER
sudo reboot
```

### 디스플레이가 업데이트되지 않음
- 전원 확인
- HAT 연결 상태 확인
- `epd.Clear()` 먼저 실행

## 7. 최적화 팁

### 배터리 절약
- 업데이트 후 `sleep()` 호출 필수
- 업데이트 간격 늘리기 (3600초 → 7200초)

### 수명 연장
- 불필요한 업데이트 최소화
- Partial update보다 Full update 권장

## 8. 참고 자료

- Waveshare Wiki: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT
- 공식 GitHub: https://github.com/waveshare/e-Paper
- Raspberry Pi 공식 가이드: https://www.raspberrypi.com/news/using-e-ink-raspberry-pi/
