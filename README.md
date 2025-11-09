# Weather E-ink Dashboard

E-ink 디스플레이를 사용한 날씨 대시보드 프로젝트입니다.

## 기능

- 한국 날씨 정보 실시간 업데이트
- E-ink 디스플레이 최적화 이미지 생성
- 매시간 자동 업데이트
- 저전력 설계

## 프로젝트 구조

```
weather_elink/
├── src/
│   ├── weather_api.py      # 날씨 API 연동
│   ├── display_generator.py # E-ink 이미지 생성
│   └── scheduler.py         # 자동 업데이트 스케줄러
├── config/
│   └── config.yaml          # 설정 파일
├── assets/
│   ├── icons/               # 날씨 아이콘
│   └── fonts/               # 폰트 파일
├── output/                  # 생성된 이미지 저장
├── requirements.txt
└── main.py
```

## 빠른 시작

### 🆕 Pimoroni Inky Impression 사용자
**INKY_SETUP_GUIDE.md** 또는 **QUICK_START.md**를 참고하세요!

### 일반 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# 하드웨어별 라이브러리 설치
pip install inky[rpi,fonts]        # Inky Impression용
# 또는
pip install waveshare-epd          # Waveshare용

# API 키 설정
cp .env.example .env
nano .env  # OPENWEATHER_API_KEY 입력

# 실행!
python main.py
```

자세한 설정은 **SETUP_GUIDE.md** 참고

## 지원 하드웨어

### 한국에서 구매 가능한 제품 ✅

**Waveshare E-Paper HAT 시리즈** (디바이스마트, 엘레파츠, 쿠팡)
- **7.5inch (800×480)** - 추천! 현재 코드와 완벽 호환 (~7만원)
- **4.2inch (400×300)** - 적당한 크기 (~4만원)
- **2.9inch (296×128)** - 테스트용 (~2.5만원)

**해외 직구** (7색 지원!)
- **Pimoroni Inky Impression 7.3"** (~20만원) ⭐ 7색!
  - 800×480 해상도
  - Black, White, Red, Yellow, Blue, Green, Orange
  - 설정 가이드: `INKY_SETUP_GUIDE.md`

**시뮬레이션 모드**
- 하드웨어 없이 이미지만 생성 (무료!)

### 📖 가이드 문서
- **QUICK_START.md** - 어디서부터 시작할지 모를 때
- **INKY_SETUP_GUIDE.md** - Inky Impression 전용 가이드
- **KOREAN_PRODUCTS.md** - 한국 제품 구매 가이드
- **SETUP_GUIDE.md** - 상세 설치 가이드
- **HARDWARE_SETUP.md** - Waveshare 하드웨어 가이드

## 라이선스

MIT
