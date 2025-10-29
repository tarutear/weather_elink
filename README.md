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

## 설치

```bash
pip install -r requirements.txt
```

## 설정

`config/config.yaml` 파일에서 다음을 설정하세요:
- 위치 (위도/경도 또는 도시명)
- API 키
- 업데이트 주기
- 디스플레이 설정

## 사용법

```bash
# 한 번 실행 (테스트용)
python main.py

# 백그라운드에서 자동 업데이트
python main.py --daemon
```

## 지원 하드웨어

### 한국에서 구매 가능한 제품 ✅

**Waveshare E-Paper HAT 시리즈** (디바이스마트, 엘레파츠, 쿠팡)
- **7.5inch (800×480)** - 추천! 현재 코드와 완벽 호환 (~7만원)
- **4.2inch (400×300)** - 적당한 크기 (~4만원)
- **2.9inch (296×128)** - 테스트용 (~2.5만원)

**해외 직구**
- Pimoroni Inky Impression 7.3" (~20만원)

**시뮬레이션 모드**
- 하드웨어 없이 이미지만 생성 (무료!)

자세한 구매 가이드는 `KOREAN_PRODUCTS.md` 참고

## 라이선스

MIT
