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
                # InkyPi 스타일: 더 큰 폰트
                self.font_xlarge = ImageFont.truetype(font_path, 100)  # 온도용
                self.font_large = ImageFont.truetype(font_path, 48)    # 헤더용
                self.font_medium = ImageFont.truetype(font_path, 32)   # 정보용
                self.font_small = ImageFont.truetype(font_path, 22)    # 레이블용
                self.font_tiny = ImageFont.truetype(font_path, 16)     # 예보용
            else:
                # 폰트를 찾지 못한 경우 기본 폰트 사용
                print("⚠️  한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
                self.font_xlarge = ImageFont.load_default()
                self.font_large = ImageFont.load_default()
                self.font_medium = ImageFont.load_default()
                self.font_small = ImageFont.load_default()
                self.font_tiny = ImageFont.load_default()

        except Exception as e:
            print(f"폰트 로드 실패: {e}")
            self.font_xlarge = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def generate_weather_display(self, current: Dict, forecast: List[Dict] = None,
                                  daily_forecast: List[Dict] = None) -> Image:
        """
        날씨 대시보드 이미지 생성

        Args:
            current: 현재 날씨 정보
            forecast: 시간별 예보 정보 리스트 (선택)
            daily_forecast: 일별 예보 정보 리스트 (선택)

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

        # 현재 날씨 (왼쪽 영역) - 큰 아이콘 + 온도
        self._draw_current_weather_large(current)

        # 세부 정보 (우측 영역) - 일출/일몰, 습도, 기압 등
        self._draw_weather_details(current)

        # 중단: 시간별 예보 타임라인 (dashimage.png 스타일)
        if forecast:
            self._draw_hourly_timeline(forecast)

        # 하단: 7일 예보
        if daily_forecast:
            self._draw_daily_forecast(daily_forecast)

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
        """헤더 그리기 (위치, 날짜/요일) - InkyPi 스타일"""
        # 현재 시간
        now = datetime.now()
        weekday_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][now.weekday()]

        # 위치 (사용자 정의 이름 또는 API 이름)
        location = current.get("display_name", current.get("location", "수원"))
        bbox = self.draw.textbbox((0, 0), location, font=self.font_large)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2

        self.draw.text(
            (x, 10),
            location,
            fill=self.COLOR_BLACK,
            font=self.font_large
        )

        # 날짜와 요일 (작은 글씨)
        date_str = now.strftime(f"%Y년 %m월 %d일 {weekday_kr}")
        bbox = self.draw.textbbox((0, 0), date_str, font=self.font_small)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2

        self.draw.text(
            (x, 65),
            date_str,
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

        # 구분선
        self.draw.line(
            [(30, 100), (self.width - 30, 100)],
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

    def _draw_current_weather_large(self, current: Dict):
        """현재 날씨 크게 그리기 (좌측 영역) - dashimage.png 스타일"""
        start_y = 115

        # 날씨 아이콘 (큰 원) - 왼쪽에 배치
        icon_x, icon_y = 110, start_y + 50
        icon_radius = 60

        # 원 그리기 (연한 회색 배경)
        self.draw.ellipse(
            [(icon_x - icon_radius, icon_y - icon_radius),
             (icon_x + icon_radius, icon_y + icon_radius)],
            fill=220, outline=self.COLOR_BLACK, width=3
        )

        # 온도 - 매우 큰 글씨 (아이콘 오른쪽 중앙)
        temp_text = f"{current['temperature']:.0f}°"
        self.draw.text(
            (icon_x + icon_radius + 30, icon_y - 50),
            temp_text,
            fill=self.COLOR_BLACK,
            font=self.font_xlarge
        )

        # 체감 온도 (온도 아래)
        feels_text = f"체감 {current['feels_like']:.0f}°"
        self.draw.text(
            (icon_x + icon_radius + 35, icon_y + 30),
            feels_text,
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

        # 날씨 설명 (아이콘 아래)
        desc = current.get("weather_description", "")
        bbox = self.draw.textbbox((0, 0), desc, font=self.font_small)
        text_width = bbox[2] - bbox[0]
        desc_x = icon_x - text_width // 2

        self.draw.text(
            (desc_x, icon_y + icon_radius + 15),
            desc,
            fill=self.COLOR_BLACK,
            font=self.font_small
        )

    def _draw_weather_details(self, current: Dict):
        """세부 날씨 정보 그리기 (우측 영역) - InkyPi 스타일"""
        details_x = self.width // 2 + 50
        start_y = 120

        # 단일 컬럼 레이아웃 (더 컴팩트하게)
        details = [
            ("일출", f"{current.get('sunrise', 'N/A')}"),
            ("일몰", f"{current.get('sunset', 'N/A')}"),
            ("습도", f"{current.get('humidity', 'N/A')}%"),
            ("기압", f"{current.get('pressure', 'N/A')} hPa"),
            ("가시거리", f"{current.get('visibility', 'N/A')} km"),
            ("풍속", f"{current.get('wind_speed', 'N/A')} m/s"),
        ]

        row_height = 35

        for i, (label, value) in enumerate(details):
            y = start_y + (i * row_height)

            # 레이블 (작고 회색조)
            self.draw.text(
                (details_x, y),
                label,
                fill=100,  # 회색
                font=self.font_tiny
            )

            # 값 (크고 진하게)
            self.draw.text(
                (details_x, y + 18),
                value,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

    def _draw_hourly_timeline(self, forecast: List[Dict]):
        """시간별 예보 타임라인 그리기 (dashimage.png 스타일)"""
        if not forecast:
            return

        # 타임라인 영역
        timeline_y = 280
        timeline_height = 70
        start_x = 40
        end_x = self.width - 40

        # 배경 영역 (연한 회색)
        self.draw.rectangle(
            [(start_x - 5, timeline_y - 5),
             (end_x + 5, timeline_y + timeline_height)],
            fill=240, outline=self.COLOR_BLACK, width=1
        )

        # 타임라인 (가로선)
        line_y = timeline_y + 35
        self.draw.line(
            [(start_x, line_y), (end_x, line_y)],
            fill=self.COLOR_BLACK, width=2
        )

        # 예보 항목 표시 (최대 12개)
        num_points = min(len(forecast), 12)
        spacing = (end_x - start_x) // (num_points - 1) if num_points > 1 else 0

        for i in range(num_points):
            f = forecast[i]
            x = start_x + (i * spacing)

            # 시간 표시 (타임라인 위)
            time_str = f.get("time", "")[:5]  # "HH:MM" 형식
            bbox = self.draw.textbbox((0, 0), time_str, font=self.font_tiny)
            text_width = bbox[2] - bbox[0]

            self.draw.text(
                (x - text_width // 2, timeline_y - 2),
                time_str,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

            # 날씨 아이콘 (작은 원)
            icon_r = 8
            self.draw.ellipse(
                [(x - icon_r, line_y - icon_r),
                 (x + icon_r, line_y + icon_r)],
                fill=self.COLOR_WHITE, outline=self.COLOR_BLACK, width=2
            )

            # 온도 표시 (타임라인 아래)
            temp_str = f"{f.get('temperature', 0):.0f}°"
            bbox = self.draw.textbbox((0, 0), temp_str, font=self.font_tiny)
            text_width = bbox[2] - bbox[0]

            self.draw.text(
                (x - text_width // 2, line_y + 15),
                temp_str,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

    def _draw_daily_forecast(self, daily_forecast: List[Dict]):
        """7일 예보 그리기 (하단 영역) - InkyPi 카드 스타일"""
        if not daily_forecast:
            return

        # 구분선 (hourly timeline 아래로 조정)
        y_line = 365
        self.draw.line(
            [(30, y_line), (self.width - 30, y_line)],
            fill=self.COLOR_BLACK,
            width=2
        )

        # 예보 카드들 (제목 제거하고 더 컴팩트하게)
        card_width = (self.width - 80) // 7
        start_x = 40
        card_y = y_line + 15

        for i, day in enumerate(daily_forecast[:7]):
            card_x = start_x + i * card_width

            # 카드 배경 (선택사항)
            # self.draw.rectangle(
            #     [(card_x - 5, card_y - 5), (card_x + card_width - 10, card_y + 80)],
            #     outline=self.COLOR_BLACK, width=1
            # )

            # 요일
            day_name = day.get("day_name_kr", day.get("day_name", ""))
            bbox = self.draw.textbbox((0, 0), day_name, font=self.font_tiny)
            text_width = bbox[2] - bbox[0]
            day_x = card_x + (card_width - text_width) // 2

            self.draw.text(
                (day_x, card_y),
                day_name,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

            # 날씨 아이콘 (작은 원) - 흰색 배경
            icon_x = card_x + card_width // 2
            icon_y = card_y + 30
            icon_r = 14
            self.draw.ellipse(
                [(icon_x - icon_r, icon_y - icon_r),
                 (icon_x + icon_r, icon_y + icon_r)],
                fill=self.COLOR_WHITE, outline=self.COLOR_BLACK, width=2
            )

            # 온도 (위/아래)
            temp_max = f"{day['temp_max']}°"
            temp_min = f"{day['temp_min']}°"

            # 최고 온도 (진하게)
            bbox = self.draw.textbbox((0, 0), temp_max, font=self.font_tiny)
            text_width = bbox[2] - bbox[0]
            temp_x = card_x + (card_width - text_width) // 2

            self.draw.text(
                (temp_x, card_y + 60),
                temp_max,
                fill=self.COLOR_BLACK,
                font=self.font_tiny
            )

            # 최저 온도 (회색)
            bbox = self.draw.textbbox((0, 0), temp_min, font=self.font_tiny)
            text_width = bbox[2] - bbox[0]
            temp_x = card_x + (card_width - text_width) // 2

            self.draw.text(
                (temp_x, card_y + 77),
                temp_min,
                fill=120,  # 회색
                font=self.font_tiny
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
