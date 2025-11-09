# 빠른 시작 가이드

## 🎯 현재 상황: Pimoroni Inky Impression 7.3" 구매 완료!

축하합니다! 7색 E-ink 디스플레이를 선택하셨네요. 이제 단계별로 진행하겠습니다.

---

## 📋 체크리스트

현재 어디까지 진행하셨나요?

- [ ] **1단계**: 하드웨어 준비 (Raspberry Pi, microSD 카드 등)
- [ ] **2단계**: Raspberry Pi OS 설치
- [ ] **3단계**: SSH 접속 성공
- [ ] **4단계**: 프로젝트 파일 복사
- [ ] **5단계**: 라이브러리 설치
- [ ] **6단계**: Inky HAT 물리적 연결
- [ ] **7단계**: 설정 파일 수정
- [ ] **8단계**: API 키 설정
- [ ] **9단계**: 테스트 실행
- [ ] **10단계**: 자동 실행 설정

---

## 🚀 어디서부터 시작할까요?

### 시나리오 A: Raspberry Pi가 아직 없어요
→ **INKY_SETUP_GUIDE.md의 1-2단계 참고**
- Raspberry Pi 구매 (Zero 2 W 또는 4B 추천)
- microSD 카드 준비
- Raspberry Pi OS 설치

### 시나리오 B: Raspberry Pi는 있는데 OS 설치 안 했어요
→ **INKY_SETUP_GUIDE.md의 2단계 참고**
- Raspberry Pi Imager로 OS 설치
- WiFi 설정 포함

### 시나리오 C: Raspberry Pi가 준비되어 있고 SSH 접속 가능해요
→ **아래 빠른 설정 명령어 사용!**

---

## ⚡ 빠른 설정 (SSH 접속 가능한 경우)

Raspberry Pi에 SSH로 접속한 상태에서 아래 명령어를 순서대로 실행하세요.

### 1️⃣ 시스템 업데이트
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y git python3-pip python3-pil python3-numpy fonts-nanum
```

### 2️⃣ 프로젝트 클론 (GitHub에서)
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/weather_elink.git
cd weather_elink
```

**또는 로컬에서 파일 복사 (본인 PC에서):**
```bash
# Windows PowerShell
scp -r C:\path\to\weather_elink pi@raspberrypi.local:~/

# Mac/Linux
scp -r ~/path/to/weather_elink pi@raspberrypi.local:~/
```

### 3️⃣ Python 가상환경 및 의존성 설치
```bash
cd ~/weather_elink
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install inky[rpi,fonts]
```

### 4️⃣ 설정 파일 준비
```bash
# Inky 전용 설정 사용
cp config/config.inky.yaml config/config.yaml

# API 키 설정
cp .env.example .env
nano .env
```

`.env` 파일에서 수정:
```bash
OPENWEATHER_API_KEY=your_actual_api_key_here
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

### 5️⃣ 전원 끄고 HAT 연결
```bash
sudo shutdown -h now
```

- Inky Impression HAT를 GPIO 핀에 조심스럽게 연결
- 전원 다시 켜기

### 6️⃣ SSH 재접속 및 테스트
```bash
ssh pi@raspberrypi.local
cd ~/weather_elink
source venv/bin/activate

# 시뮬레이션 모드로 이미지 먼저 생성
nano config/config.yaml
# mode를 "simulation"으로 변경
python main.py

# 성공하면 하드웨어 모드로 전환
nano config/config.yaml
# mode를 "hardware"로 변경
# display_type을 "inky"로 변경

# 실제 디스플레이 테스트!
python main.py
```

### 7️⃣ 자동 실행 설정 (선택사항)
```bash
sudo nano /etc/systemd/system/weather-dashboard.service
```

다음 내용 입력:
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

활성화:
```bash
sudo systemctl daemon-reload
sudo systemctl enable weather-dashboard.service
sudo systemctl start weather-dashboard.service
sudo systemctl status weather-dashboard.service
```

---

## 📚 상세 가이드 문서

### 🆕 Inky Impression 전용
- **INKY_SETUP_GUIDE.md** - 가장 자세한 단계별 가이드 (추천!)

### 일반 설정
- **SETUP_GUIDE.md** - 소프트웨어 설치 가이드
- **HARDWARE_SETUP.md** - Waveshare 하드웨어 가이드
- **KOREAN_PRODUCTS.md** - 한국 제품 구매 가이드

---

## ❓ 자주 묻는 질문

### Q: Raspberry Pi 어떤 모델을 사야 하나요?
**A:**
- **추천**: Raspberry Pi Zero 2 W (저전력, 충분한 성능)
- **대안**: Raspberry Pi 4B (강력하지만 전력 소비 큼)
- **중요**: "With Headers" 버전 구매!

### Q: API 키는 어디서 받나요?
**A:**
1. https://openweathermap.org/ 접속
2. 무료 회원가입
3. API Keys 메뉴에서 복사
4. `.env` 파일에 붙여넣기

### Q: 7색이 제대로 표시되나요?
**A:** 네! Inky Impression은 다음 7색을 지원합니다:
- Black, White, Red, Yellow, Blue, Green, Orange
- 자동으로 최적의 색상으로 변환됩니다

### Q: 업데이트가 너무 느려요
**A:** E-ink 특성상 정상입니다:
- Inky Impression: 약 30초 소요
- 배터리 절약을 위해 의도적으로 느림
- 1시간마다 업데이트면 충분합니다

### Q: 에러가 발생해요
**A:**
1. 로그 확인: `journalctl -u weather-dashboard.service -f`
2. API 키 확인: `cat .env`
3. 라이브러리 재설치: `pip install --upgrade inky[rpi,fonts]`
4. 권한 확인: `sudo usermod -a -G spi,gpio,i2c pi`

---

## 🆘 도움이 필요하신가요?

**현재 진행 상황을 알려주세요:**
1. Raspberry Pi가 있나요?
2. OS는 설치했나요?
3. SSH 접속이 되나요?
4. 어느 단계에서 막혔나요?

**구체적으로 알려주시면 맞춤형 도움을 드리겠습니다!**

---

## ✅ 성공 확인

다음이 모두 작동하면 성공입니다:

- [ ] `python main.py` 실행 시 날씨 정보 출력
- [ ] `output/` 폴더에 이미지 생성
- [ ] Inky Impression에 7색으로 날씨 표시
- [ ] 매시간 자동 업데이트
- [ ] 재부팅 후에도 자동 시작

**축하합니다! 🎉**

---

다음 단계는 무엇인가요? 알려주시면 도와드리겠습니다! 😊
