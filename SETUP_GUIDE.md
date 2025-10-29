# 설치 및 사용 가이드

## 1. 시스템 요구사항

- Python 3.7 이상
- pip (Python 패키지 관리자)
- 인터넷 연결 (날씨 API 호출용)

## 2. 설치 단계

### 2.1 저장소 클론 (또는 다운로드)

```bash
git clone <repository-url>
cd weather_elink
```

### 2.2 Python 가상환경 생성 (권장)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 2.3 의존성 설치

```bash
pip install -r requirements.txt
```

### 2.4 한글 폰트 설치 (Linux)

Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install fonts-nanum fonts-nanum-coding
```

Raspberry Pi:
```bash
sudo apt-get install fonts-nanum
```

## 3. API 키 발급

### OpenWeatherMap API 키 발급

1. https://openweathermap.org/ 방문
2. 회원가입 (무료)
3. API Keys 메뉴에서 키 복사
4. 무료 플랜: 1,000 calls/day (충분함)

## 4. 설정

### 4.1 환경변수 설정

`.env.example` 파일을 복사하여 `.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```bash
# OpenWeatherMap API 키 입력
OPENWEATHER_API_KEY=your_actual_api_key_here

# 도시 설정 (한국 주요 도시)
OPENWEATHER_CITY=Seoul  # 또는 Busan, Incheon, Daegu, Gwangju 등

# 위치 좌표 (더 정확한 날씨 정보)
LATITUDE=37.5665  # 서울 기준
LONGITUDE=126.9780
```

### 4.2 한국 주요 도시 좌표

| 도시 | 위도 | 경도 |
|------|------|------|
| 서울 | 37.5665 | 126.9780 |
| 부산 | 35.1796 | 129.0756 |
| 인천 | 37.4563 | 126.7052 |
| 대구 | 35.8714 | 128.6014 |
| 대전 | 36.3504 | 127.3845 |
| 광주 | 35.1595 | 126.8526 |
| 울산 | 35.5384 | 129.3114 |
| 제주 | 33.4996 | 126.5312 |

### 4.3 config.yaml 설정 (선택사항)

`config/config.yaml` 파일에서 세부 설정 조정:

```yaml
location:
  city: "Seoul"
  latitude: 37.5665
  longitude: 126.9780

display:
  width: 800
  height: 480

weather_api:
  update_interval: 3600  # 1시간 (초 단위)
```

## 5. 실행 방법

### 5.1 한 번만 실행 (테스트)

```bash
python main.py
```

결과: `output/` 폴더에 날씨 이미지 생성

### 5.2 자동 업데이트 모드 (매시간)

```bash
python main.py --daemon
```

종료: `Ctrl + C`

## 6. 테스트

### 6.1 날씨 API 테스트

```bash
python src/weather_api.py
```

### 6.2 이미지 생성 테스트

```bash
python src/display_generator.py
```

### 6.3 스케줄러 테스트

```bash
python src/scheduler.py
```

## 7. Raspberry Pi에서 부팅 시 자동 실행

### 7.1 systemd 서비스 생성

`weather-dashboard.service` 파일 생성:

```bash
sudo nano /etc/systemd/system/weather-dashboard.service
```

내용:

```ini
[Unit]
Description=Weather E-ink Dashboard
After=network.target

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

### 7.2 서비스 활성화

```bash
sudo systemctl daemon-reload
sudo systemctl enable weather-dashboard.service
sudo systemctl start weather-dashboard.service
```

### 7.3 서비스 상태 확인

```bash
sudo systemctl status weather-dashboard.service
```

### 7.4 로그 확인

```bash
journalctl -u weather-dashboard.service -f
```

## 8. 문제 해결

### API 키 오류

```
❌ 오류: OPENWEATHER_API_KEY가 설정되지 않았습니다.
```

해결: `.env` 파일에 올바른 API 키 입력

### 한글 깨짐

해결: 한글 폰트 설치 (위 2.4 참고)

### 이미지가 생성되지 않음

1. 인터넷 연결 확인
2. API 키 유효성 확인
3. output 폴더 권한 확인

```bash
chmod 755 output
```

## 9. 하드웨어 연결 (E-ink 디스플레이)

하드웨어가 준비되면:

1. `config/config.yaml`에서 `display.mode`를 `hardware`로 변경
2. E-ink 디스플레이 라이브러리 설치
3. `main.py`의 `_update_hardware_display()` 함수 구현

### Waveshare E-Paper 예제

```bash
# Waveshare 라이브러리 설치
git clone https://github.com/waveshare/e-Paper.git
cd e-Paper/RaspberryPi_JetsonNano/python
sudo python setup.py install
```

### Pimoroni Inky Impression 예제

```bash
# Inky 라이브러리 설치
pip install inky[rpi,fonts]
```

## 10. 다음 단계

1. ✅ 기본 설정 완료
2. ✅ 날씨 정보 테스트
3. ✅ 이미지 생성 확인
4. ⏳ E-ink 디스플레이 연결
5. ⏳ 하드웨어 모드 구현
6. ⏳ UI 커스터마이징

궁금한 점이 있으면 이슈를 생성해주세요!
