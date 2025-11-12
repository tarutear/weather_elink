"""
HTML 템플릿 기반 디스플레이 렌더러
Jinja2 템플릿으로 디자인한 대시보드를 이미지로 변환
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
import tempfile


class HTMLRenderer:
    """HTML 템플릿을 이미지로 렌더링"""

    def __init__(self, template_dir: str = "templates"):
        """
        HTMLRenderer 초기화

        Args:
            template_dir: 템플릿 디렉토리 경로
        """
        self.template_dir = Path(template_dir)
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    def render_dashboard(self, current: Dict, daily_forecast: List[Dict] = None,
                        output_path: str = None) -> str:
        """
        대시보드 HTML을 렌더링하고 이미지로 변환

        Args:
            current: 현재 날씨 정보
            daily_forecast: 일별 예보 정보
            output_path: 출력 이미지 경로

        Returns:
            생성된 이미지 파일 경로
        """
        # 날짜/시간 정보
        now = datetime.now()
        weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][now.weekday()]
        date_str = now.strftime(f"%Y년 %m월 %d일 ({weekday_kr})")

        # 템플릿 로드
        template = self.env.get_template('dashboard_template.html')

        # HTML 렌더링
        html_content = template.render(
            current=current,
            daily_forecast=daily_forecast,
            date_str=date_str
        )

        # HTML을 이미지로 변환
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/weather_{timestamp}.png"

        # Playwright로 HTML → 이미지 변환
        self._html_to_image(html_content, output_path)

        return output_path

    def _html_to_image(self, html_content: str, output_path: str):
        """
        HTML을 이미지로 변환 (playwright 사용)

        Args:
            html_content: HTML 콘텐츠
            output_path: 출력 이미지 경로
        """
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # 브라우저 실행
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={'width': 800, 'height': 480})

                # HTML 콘텐츠 설정
                page.set_content(html_content)

                # 이미지로 캡처
                page.screenshot(path=output_path, full_page=False)

                browser.close()

            print(f"✅ HTML 렌더링 완료: {output_path}")

        except ImportError:
            print("⚠️  Playwright가 설치되지 않았습니다.")
            print("다음 명령으로 설치하세요:")
            print("  pip install playwright")
            print("  playwright install chromium")
            raise

        except Exception as e:
            print(f"❌ HTML 렌더링 실패: {e}")
            # Fallback: PIL 기반 렌더러 사용
            print("⚠️  PIL 기반 렌더러로 전환합니다...")
            self._fallback_to_pil(html_content, output_path)

    def _fallback_to_pil(self, html_content: str, output_path: str):
        """
        PIL 기반 폴백 렌더러

        Args:
            html_content: HTML 콘텐츠
            output_path: 출력 이미지 경로
        """
        from PIL import Image, ImageDraw, ImageFont

        # 간단한 에러 이미지 생성
        image = Image.new('RGB', (800, 480), 'white')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 24)
        except:
            font = ImageFont.load_default()

        text = "HTML 렌더링 실패\nPlaywright를 설치해주세요."
        draw.text((300, 200), text, fill='black', font=font)

        image.save(output_path)
        print(f"⚠️  폴백 이미지 생성됨: {output_path}")


def test_html_renderer():
    """HTML 렌더러 테스트"""
    from src.weather_api import WeatherAPI
    from dotenv import load_dotenv
    import os

    load_dotenv()

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ API 키가 설정되지 않았습니다.")
        return

    # 날씨 정보 가져오기
    weather_api = WeatherAPI(api_key, "Suwon", "KR")
    current = weather_api.get_current_weather(lat=37.259096, lon=127.079442)
    daily_forecast = weather_api.get_daily_forecast(lat=37.259096, lon=127.079442, days=7)

    # HTML 렌더링
    renderer = HTMLRenderer()
    output_path = renderer.render_dashboard(current, daily_forecast)

    print(f"\n✅ 테스트 완료!")
    print(f"이미지: {output_path}")


if __name__ == "__main__":
    test_html_renderer()
