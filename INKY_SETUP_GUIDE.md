# Pimoroni Inky Impression 7.3" 설정 가이드

완벽한 선택입니다! Inky Impression은 7색을 지원하는 아름다운 E-ink 디스플레이입니다.

---

## 📦 1단계: 하드웨어 및 준비물 확인

### 필요한 것들

#### ✅ 체크리스트
```
□ Pimoroni Inky Impression 7.3" (구매 완료!)
□ Raspberry Pi (Zero 2 W, 3, 4, 또는 5)
  - 추천: Pi Zero 2 W (저전력) 또는 Pi 4B
  - ⚠️ GPIO 헤더 필수 (With Headers 버전)
□ microSD 카드 (16GB 이상)
□ 전원 어댑터
  - Pi Zero: 5V 2.5A
  - Pi 4: 5V 3A (공식 어댑터 권장)
□ microSD 카드 리더기 (PC에 연결용)
□ (선택) 케이블: microHDMI, USB 키보드/마우스
□ (선택) WiFi 환경
```

---

## 💿 2단계: Raspberry Pi OS 설치

### 2-1. Raspberry Pi Imager 다운로드

**Windows/Mac/Linux:**
- https://www.raspberrypi.com/software/ 방문
- Raspberry Pi Imager 다운로드 및 설치

### 2-2. OS 이미지 작성

#### Imager 실행 후:

1. **Raspberry Pi Device 선택**
   - 본인의 Raspberry Pi 모델 선택

2. **Operating System 선택**
   ```
   Raspberry Pi OS (64-bit)
   또는
   Raspberry Pi OS Lite (64-bit) - 추천! (GUI 없음, 더 빠름)
   ```

3. **Storage 선택**
   - microSD 카드 선택

4. **⚙️ 설정 (톱니바퀴 아이콘 클릭) - 중요!**
   ```
   ✅ Set hostname: weatherdash (원하는 이름)
   ✅ Enable SSH: Use password authentication 체크
   ✅ Set username and password:
      - Username: pi
      - Password: (본인이 기억할 비밀번호)
   ✅ Configure wireless LAN:
      - SSID: (본인의 WiFi 이름)
      - Password: (WiFi 비밀번호)
      - Wireless LAN country: KR
   ✅ Set locale settings:
      - Time zone: Asia/Seoul
      - Keyboard layout: us (또는 kr)
   ```

5. **Write 클릭**
   - 확인 후 작성 시작 (5-10분 소요)

### 2-3. SD 카드 삽입 및 부팅

1. microSD 카드를 Raspberry Pi에 삽입
2. 전원 연결 → 부팅 (약 1-2분)
3. WiFi에 자동 연결됨

---

## 🔌 3단계: SSH로 Raspberry Pi 접속

### 3-1. IP 주소 확인

**방법 1: 라우터 관리 페이지**
- 공유기 설정에서 연결된 기기 확인
- `weatherdash` 또는 `raspberrypi` 이름 찾기

**방법 2: IP 스캐너 앱**
- Windows: Advanced IP Scanner
- Mac: LanScan
- 스마트폰: Fing 앱

**방법 3: 호스트네임 사용 (가장 쉬움!)**
```
weatherdash.local
```

### 3-2. SSH 접속

#### Windows (PowerShell 또는 CMD):
```bash
ssh pi@weatherdash.local
# 또는
ssh pi@192.168.0.XXX
```

#### Mac/Linux (터미널):
```bash
ssh pi@weatherdash.local
```

#### 비밀번호 입력
- 위에서 설정한 비밀번호 입력

#### 처음 접속 시:
```
The authenticity of host... (yes/no)?
→ yes 입력
```

### 접속 성공!
```
pi@weatherdash:~ $
```

---

## 🔄 4단계: 시스템 업데이트

```bash
# 시스템 패키지 업데이트 (5-10분 소요)
sudo apt-get update
sudo apt-get upgrade -y

# 필요한 시스템 패키지 설치
sudo apt-get install -y git python3-pip python3-pil python3-numpy

# 한글 폰트 설치
sudo apt-get install -y fonts-nanum fonts-nanum-coding
```

---

## 📁 5단계: 프로젝트 파일 전송

### 방법 1: Git Clone (GitHub에 올렸다면)

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/weather_elink.git
cd weather_elink
```

### 방법 2: SCP로 파일 전송 (로컬 개발 중이라면)

#### 본인의 PC에서 (새 터미널):

```bash
# Windows (PowerShell)
scp -r C:\Users\YOUR_NAME\weather_elink pi@weatherdash.local:~/

# Mac/Linux
scp -r ~/weather_elink pi@weatherdash.local:~/
```

---

## 🐍 6단계: Python 의존성 설치

```bash
# weather_elink 폴더로 이동
cd ~/weather_elink

# 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

---

## 🎨 7단계: Inky Impression 라이브러리 설치

```bash
# Inky 라이브러리 설치 (폰트 포함)
pip install inky[rpi,fonts]

# 또는 최신 버전
pip install --upgrade inky[rpi,fonts]
```

### 테스트: Inky 예제 실행

```bash
# Inky 테스트 스크립트
python3 -c "from inky.auto import auto; print('Inky library OK!')"
```

성공 시: `Inky library OK!` 출력

---

## 🔌 8단계: Inky Impression HAT 물리적 연결

### ⚠️ 전원 끄기 필수!

```bash
sudo shutdown -h now
```

### 연결 방법

1. Raspberry Pi 전원 완전히 차단
2. Inky Impression HAT를 Raspberry Pi GPIO 핀에 **조심스럽게** 연결
   - 40핀 전체가 정확히 맞아야 함
   - 한쪽으로 치우치지 않도록 주의
3. 꾹 눌러서 완전히 장착
4. 전원 다시 연결

### 부팅 후 SSH 재접속

```bash
ssh pi@weatherdash.local
cd ~/weather_elink
source venv/bin/activate
```

---

## 🔧 9단계: Inky용 디스플레이 모듈 생성

Inky Impression은 Waveshare와 다른 라이브러리를 사용하므로 별도 모듈이 필요합니다.

### Inky 디스플레이 모듈 생성:

```bash
nano src/inky_display.py
```

다음 내용 붙여넣기:

```python
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

    if not INKY_AVAILABLE:
        print("❌ Inky 라이브러리가 설치되지 않았습니다.")
        print("\n설치 방법:")
        print("  pip install inky[rpi,fonts]")
        return

    # 테스트 이미지 찾기
    import glob
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
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## ⚙️ 10단계: 설정 파일 수정

```bash
nano config/config.yaml
```

다음과 같이 수정:

```yaml
display:
  width: 800
  height: 480
  mode: "hardware"        # simulation → hardware로 변경!
  color_mode: "7color"    # 7색 모드!
  rotation: 0
  display_type: "inky"    # 새로 추가: "inky" 또는 "waveshare"
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## 🔑 11단계: API 키 설정

```bash
# .env 파일 생성
cp .env.example .env
nano .env
```

다음 내용 수정:

```bash
# OpenWeatherMap API 키 입력
OPENWEATHER_API_KEY=your_actual_api_key_here

# 위치 설정
OPENWEATHER_CITY=Seoul
LATITUDE=37.5665
LONGITUDE=126.9780
```

### API 키 발급 (아직 없다면):
1. https://openweathermap.org/ 방문
2. 회원가입 (무료)
3. API Keys 메뉴에서 키 복사
4. 위 `.env` 파일에 붙여넣기

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## 🧪 12단계: 테스트 실행

### 12-1. 이미지 생성 테스트 (시뮬레이션)

```bash
# 먼저 config.yaml을 simulation으로 설정
nano config/config.yaml
# mode: "simulation"으로 변경

# 이미지 생성 테스트
python main.py

# 성공하면 output/ 폴더에 이미지 생성됨
ls -lh output/
```

### 12-2. Inky 디스플레이 테스트

```bash
# config.yaml을 hardware로 변경
nano config/config.yaml
# mode: "hardware"
# display_type: "inky"

# main.py 수정 필요 (Inky 통합)
```

### main.py에 Inky 지원 추가:

```bash
nano main.py
```

`_update_hardware_display` 함수를 다음과 같이 수정:

```python
def _update_hardware_display(self, filepath: str):
    """하드웨어 디스플레이 업데이트"""
    print("\n🔌 하드웨어 디스플레이 업데이트...")

    try:
        display_type = self.config["display"].get("display_type", "waveshare")

        if display_type == "inky":
            # Pimoroni Inky Impression
            from src.inky_display import InkyDisplay
            display = InkyDisplay()
            display.display_image(filepath)

        else:
            # Waveshare E-Paper
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

    except Exception as e:
        print(f"❌ 디스플레이 업데이트 실패: {e}")
        import traceback
        traceback.print_exc()
```

저장 후:

```bash
# 실제 하드웨어 테스트!
python main.py
```

### 성공하면:
- 날씨 정보 가져옴
- 이미지 생성
- **Inky Impression에 7색으로 표시!** 🎨

---

## 🚀 13단계: 자동 실행 설정

매시간 자동으로 업데이트하려면:

```bash
# systemd 서비스 파일 생성
sudo nano /etc/systemd/system/weather-dashboard.service
```

다음 내용 붙여넣기:

```ini
[Unit]
Description=Weather E-ink Dashboard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/weather_elink
Environment="PATH=/home/pi/weather_elink/venv/bin"
ExecStart=/home/pi/weather_elink/venv/bin/python main.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

저장 후:

```bash
# 서비스 활성화
sudo systemctl daemon-reload
sudo systemctl enable weather-dashboard.service
sudo systemctl start weather-dashboard.service

# 상태 확인
sudo systemctl status weather-dashboard.service
```

### 로그 확인:
```bash
# 실시간 로그 보기
journalctl -u weather-dashboard.service -f

# 종료: Ctrl+C
```

---

## ✅ 완료!

축하합니다! 이제 Inky Impression 날씨 대시보드가 작동합니다!

### 확인사항:
- [ ] 날씨 정보가 7색으로 표시됨
- [ ] 매시간 자동 업데이트
- [ ] 재부팅 후에도 자동 시작

### 문제 해결:

**디스플레이가 업데이트 안 됨:**
```bash
# Inky 라이브러리 재설치
pip uninstall inky
pip install inky[rpi,fonts]
```

**권한 오류:**
```bash
# pi 사용자를 필요한 그룹에 추가
sudo usermod -a -G spi,gpio,i2c pi
sudo reboot
```

**API 오류:**
```bash
# .env 파일 확인
cat .env
# API 키가 제대로 입력되었는지 확인
```

---

## 🎨 다음 단계 (선택사항)

### UI 커스터마이징
- `src/display_generator.py` 수정
- 색상 활용도 개선 (7색!)
- 레이아웃 변경

### 추가 정보 표시
- 미세먼지 정보
- 자외선 지수
- 주간 예보

### 케이스 제작
- 3D 프린팅 케이스
- 액자 형태로 벽에 걸기

---

궁금한 점이나 문제가 있으면 언제든 물어보세요! 🙌
