# 한국에서 구매 가능한 E-ink 제품 가이드

## 🛒 온라인 구매처

### 1. 엘레파츠 (eleparts.co.kr)
- Waveshare 공식 파트너
- 빠른 배송 (1-2일)
- 기술 지원 우수

**추천 제품:**
- Waveshare 7.5inch E-Paper HAT (B/W)
- Waveshare 7.5inch E-Paper HAT (B/W/R)

### 2. 디바이스마트 (devicemart.co.kr)
- Raspberry Pi 전문 쇼핑몰
- E-Paper 제품 다수 보유
- 기술 문서 제공

### 3. 아이씨뱅큐 (icbanq.com)
- 해외 제품 수입 전문
- 다양한 Waveshare 제품

### 4. 쿠팡 / 네이버쇼핑
- 검색어: "Waveshare E-Paper"
- 로켓배송 가능 제품 있음
- 가격 비교 용이

---

## 📱 제품별 상세 정보

### ⭐ 추천 #1: Waveshare 7.5inch E-Paper HAT

#### 제품 코드: 7.5inch e-Paper HAT

**사양:**
```
해상도: 800 × 480 pixels
크기: 7.5 inch
색상: 흑백 (Black/White)
인터페이스: SPI
소비전력: <0.01W (대기)
Refresh: ~6초
가격: 약 65,000 ~ 75,000원
```

**장점:**
- ✅ 현재 코드와 완벽 호환 (800×480)
- ✅ 코드 수정 없이 바로 사용 가능
- ✅ 큰 화면으로 정보 표시 여유
- ✅ 국내 구매 용이
- ✅ 문서/예제 풍부

**단점:**
- 리프레시 속도 느림 (E-ink 특성)
- 색상 표현 제한 (흑백만)

**구매 링크 검색어:**
```
엘레파츠 Waveshare 7.5inch e-Paper HAT
디바이스마트 7.5인치 전자종이
```

---

### 추천 #2: Waveshare 7.5inch E-Paper HAT (B/W/R)

**사양:**
```
해상도: 800 × 480 pixels
크기: 7.5 inch
색상: 3색 (Black/White/Red)
가격: 약 75,000 ~ 85,000원
```

**장점:**
- ✅ 빨간색 강조 가능 (경고, 중요 정보)
- ✅ 시각적으로 더 매력적

**단점:**
- 리프레시 더 느림 (~16초)
- 가격 약간 높음

---

### 예산형: Waveshare 4.2inch E-Paper HAT

**사양:**
```
해상도: 400 × 300 pixels
크기: 4.2 inch
가격: 약 38,000 ~ 45,000원
```

**설정 변경:**

`config/config.yaml`:
```yaml
display:
  width: 400
  height: 300
  epaper_model: "4in2"
```

**적합한 용도:**
- 책상 위 미니 날씨 알림판
- 전력 소비 최소화
- 예산 제한 있을 때

---

### 입문용: Waveshare 2.9inch E-Paper HAT

**사양:**
```
해상도: 296 × 128 pixels
크기: 2.9 inch
가격: 약 23,000 ~ 28,000원
```

**설정 변경:**

`config/config.yaml`:
```yaml
display:
  width: 296
  height: 128
  epaper_model: "2in9_V2"
```

**적합한 용도:**
- 첫 E-ink 프로젝트
- 테스트/학습용
- 초저전력 필요시

---

## 💻 Raspberry Pi 보드 선택

### Raspberry Pi Zero 2 W (추천!)
```
가격: 약 25,000원
장점:
- 저전력 (<1W)
- 작은 크기
- WiFi 내장
- 충분한 성능
```

### Raspberry Pi 4B
```
가격: 약 60,000 ~ 80,000원
장점:
- 강력한 성능
- 여러 용도 병행 가능
단점:
- 전력 소비 큼
- 날씨 대시보드에는 오버스펙
```

---

## 📦 전체 구매 리스트 (초보자용)

### 기본 구성 (~100,000원)
```
□ Waveshare 7.5" E-Paper HAT ... 70,000원
□ Raspberry Pi Zero 2 W ......... 25,000원
□ microSD 카드 (16GB+) ............ 8,000원
□ USB 전원 어댑터 (5V 2.5A) ..... 5,000원
□ microUSB 케이블 .................. 3,000원
────────────────────────────────────
합계: 약 111,000원
```

### 프리미엄 구성 (~150,000원)
```
□ Waveshare 7.5" E-Paper (B/W/R) 80,000원
□ Raspberry Pi 4B (2GB) ........... 60,000원
□ microSD 카드 (32GB) .............. 12,000원
□ 공식 전원 어댑터 ................. 10,000원
□ 케이스 ................................ 8,000원
────────────────────────────────────
합계: 약 170,000원
```

---

## 🔍 제품 찾기 팁

### 엘레파츠에서 찾기
1. eleparts.co.kr 접속
2. 검색: "Waveshare e-paper"
3. 필터: Display > E-Paper
4. 해상도 확인 필수!

### 디바이스마트에서 찾기
1. devicemart.co.kr 접속
2. 카테고리: 디스플레이 > E-ink/E-Paper
3. 제조사: Waveshare 필터

### 쿠팡에서 찾기
1. 검색: "Waveshare 7.5 e-paper"
2. 로켓배송 제품 우선
3. 리뷰 확인!
4. **주의**: 가격이 너무 싸면 짝퉁 가능성

---

## ⚠️ 구매 시 주의사항

### 1. 버전 확인
- V2, V3 등 버전 차이 있음
- 최신 버전 권장 (리프레시 속도 개선)

### 2. HAT vs 모듈
- **HAT**: Raspberry Pi GPIO에 바로 꽂는 형태 (추천!)
- **모듈**: 배선 필요 (초보자 비추천)

### 3. SPI 인터페이스 확인
- 대부분 SPI 방식
- UART 방식은 피할 것

### 4. 호환성 확인
```python
# 이 프로젝트가 지원하는 모델
지원: 7in5_V2, 4in2, 2in9_V2
미지원: UART 방식, GoodDisplay 브랜드
```

---

## 🛠️ 구매 후 다음 단계

1. **하드웨어 조립**
   - E-Paper HAT를 Raspberry Pi에 연결
   - HARDWARE_SETUP.md 참고

2. **소프트웨어 설정**
   ```bash
   pip install waveshare-epd
   ```

3. **config.yaml 수정**
   ```yaml
   display:
     mode: "hardware"
   ```

4. **실행!**
   ```bash
   python main.py
   ```

---

## 💡 절약 팁

### 중고 구매
- 당근마켓, 중고나라에서 검색
- Raspberry Pi Zero는 중고도 OK
- E-Paper는 새 제품 권장

### 일단 시뮬레이션
- 하드웨어 없이 먼저 개발
- output/ 폴더에 이미지 생성
- 타블렛/모니터로 확인
- 만족하면 하드웨어 구매

### 단계별 구매
1. 단계: Raspberry Pi만 구매 (다른 프로젝트 겸용)
2. 단계: 작은 E-Paper로 테스트 (2.9")
3. 단계: 만족하면 큰 E-Paper 구매 (7.5")

---

## 📞 문의처

### 엘레파츠
- 웹사이트: eleparts.co.kr
- 고객센터: 게시판 문의

### 디바이스마트
- 웹사이트: devicemart.co.kr
- 전화: 02-776-4868

### 기술 지원
- Waveshare Wiki: waveshare.com/wiki
- 이 프로젝트 Issues: GitHub

---

## 🎯 결론 및 추천

**초보자라면:**
→ Waveshare 7.5" + Raspberry Pi Zero 2 W

**예산이 부족하다면:**
→ 일단 시뮬레이션 모드로 시작 (무료!)

**최고 품질을 원한다면:**
→ Pimoroni Inky Impression (해외직구)

**가장 경제적:**
→ Waveshare 2.9" (2만원대)

---

**이 프로젝트는 모든 해상도를 지원합니다!**
config.yaml만 수정하면 어떤 E-Paper도 사용 가능합니다.
