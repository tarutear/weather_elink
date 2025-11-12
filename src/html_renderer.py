"""
HTML 템플릿 기반 디스플레이 렌더러
Jinja2 템플릿으로 디자인한 대시보드를 이미지로 변환
wkhtmltoimage 사용 (라즈베리파이 Zero 2 W 최적화)
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
import tempfile
import subprocess
import os


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

        # 렌더링 방법 확인
        self.render_method = self._detect_render_method()

    def _detect_render_method(self) -> str:
        """사용 가능한 렌더링 방법 탐지"""
        # WeasyPrint 확인 (최우선 - 경량이고 Python native)
        try:
            import weasyprint
            print("✅ WeasyPrint 감지됨 (경량 모드, Pi Zero 2 W 최적화)")
            return 'weasyprint'
        except ImportError:
            pass

        # wkhtmltoimage 확인
        try:
            result = subprocess.run(['which', 'wkhtmltoimage'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ wkhtmltoimage 감지됨")
                return 'wkhtmltoimage'
        except:
            pass

        # chromium 확인
        for cmd in ['chromium-browser', 'chromium', 'google-chrome']:
            try:
                result = subprocess.run(['which', cmd],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ {cmd} 감지됨")
                    return 'chromium'
            except:
                continue

        print("⚠️  렌더링 도구를 찾을 수 없습니다. PIL 폴백 사용")
        return 'pil'

    def render_dashboard(self, current: Dict, forecast: List[Dict] = None,
                        daily_forecast: List[Dict] = None, output_path: str = None) -> str:
        """
        대시보드 HTML을 렌더링하고 이미지로 변환

        Args:
            current: 현재 날씨 정보
            forecast: 시간별 예보 정보
            daily_forecast: 일별 예보 정보
            output_path: 출력 이미지 경로

        Returns:
            생성된 이미지 파일 경로
        """
        # 날짜/시간 정보
        now = datetime.now()
        weekday_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][now.weekday()]
        date_str = now.strftime(f"%A, %B %d")  # Sunday, March 09 스타일

        # 위치 (사용자 정의 이름)
        location = current.get("display_name", current.get("location", "수원"))

        # 시간별 예보 준비 (최대 12개)
        hourly_forecast = []
        if forecast:
            for i, f in enumerate(forecast[:12]):
                time_str = f.get("time", "")
                if ":" in time_str:
                    hour = int(time_str.split(":")[0])
                    period = "AM" if hour < 12 else "PM"
                    display_hour = hour if hour <= 12 else hour - 12
                    display_hour = 12 if display_hour == 0 else display_hour
                    time_display = f"{display_hour} {period}"
                else:
                    time_display = time_str

                hourly_forecast.append({
                    'time': time_display,
                    'temp': f"{f.get('temperature', 0):.0f}",
                    'icon': '☀' if 'clear' in f.get('weather_description', '').lower() else '☁'
                })

        # 일별 예보 준비
        daily_data = []
        if daily_forecast:
            for day in daily_forecast[:7]:
                day_name = day.get('day_name_kr', day.get('day_name', ''))
                daily_data.append({
                    'name': day_name,
                    'temp_max': f"{day.get('temp_max', 0):.0f}",
                    'temp_min': f"{day.get('temp_min', 0):.0f}",
                    'icon': '☀' if 'clear' in day.get('weather_description', '').lower() else '☁'
                })

        # 템플릿 로드
        template = self.env.get_template('weather_dashboard.html')

        # HTML 렌더링
        html_content = template.render(
            location=location,
            date=date_str,
            temperature=f"{current.get('temperature', 0):.0f}",
            feels_like=f"{current.get('feels_like', 0):.0f}",
            sunrise=current.get('sunrise', 'N/A'),
            sunset=current.get('sunset', 'N/A'),
            humidity=current.get('humidity', 'N/A'),
            pressure=current.get('pressure', 'N/A'),
            visibility=current.get('visibility', 'N/A'),
            wind_speed=current.get('wind_speed', 'N/A'),
            hourly_forecast=hourly_forecast,
            daily_forecast=daily_data
        )

        # HTML을 이미지로 변환
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/weather_{timestamp}.png"

        # 출력 디렉토리 생성
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        # 렌더링 방법에 따라 변환
        self._html_to_image(html_content, output_path)

        return output_path

    def _html_to_image(self, html_content: str, output_path: str):
        """
        HTML을 이미지로 변환

        Args:
            html_content: HTML 콘텐츠
            output_path: 출력 이미지 경로
        """
        if self.render_method == 'weasyprint':
            self._render_with_weasyprint(html_content, output_path)
        elif self.render_method == 'wkhtmltoimage':
            self._render_with_wkhtmltoimage(html_content, output_path)
        elif self.render_method == 'chromium':
            self._render_with_chromium(html_content, output_path)
        else:
            print("⚠️  HTML 렌더링 도구가 없습니다. PIL 폴백 사용")
            self._fallback_to_pil(html_content, output_path)

    def _render_with_weasyprint(self, html_content: str, output_path: str):
        """WeasyPrint로 렌더링 (Python native, 경량)"""
        try:
            from weasyprint import HTML
            from PIL import Image
            import io

            # HTML 객체 생성
            html = HTML(string=html_content)

            # PNG로 직접 렌더링 (weasyprint 60.0+)
            try:
                # 최신 버전: write_png() 사용
                png_bytes = html.write_png()

                # PIL로 열어서 800x480 크기 조정
                img = Image.open(io.BytesIO(png_bytes))
                img = img.resize((800, 480), Image.Resampling.LANCZOS)
                img.save(output_path, 'PNG')

            except AttributeError:
                # 구버전: PDF를 거쳐서 변환
                pdf_bytes = html.write_pdf()

                # pdf2image로 변환
                try:
                    from pdf2image import convert_from_bytes
                    images = convert_from_bytes(pdf_bytes, fmt='png', size=(800, 480))
                    if images:
                        images[0].save(output_path, 'PNG')
                except ImportError:
                    raise Exception("pdf2image가 필요합니다: pip install pdf2image")

            print(f"✅ HTML 렌더링 완료 (WeasyPrint): {output_path}")

        except Exception as e:
            print(f"❌ WeasyPrint 렌더링 실패: {e}")
            print("   PIL 폴백으로 전환합니다...")
            self._fallback_to_pil(html_content, output_path)

    def _render_with_wkhtmltoimage(self, html_content: str, output_path: str):
        """wkhtmltoimage로 렌더링 (가장 경량)"""
        try:
            # 임시 HTML 파일 생성
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                temp_html = f.name

            # wkhtmltoimage 실행
            cmd = [
                'wkhtmltoimage',
                '--width', '800',
                '--height', '480',
                '--quality', '100',
                '--quiet',
                temp_html,
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            # 임시 파일 삭제
            os.unlink(temp_html)

            if result.returncode == 0:
                print(f"✅ HTML 렌더링 완료: {output_path}")
            else:
                raise Exception(f"wkhtmltoimage 실패: {result.stderr}")

        except Exception as e:
            print(f"❌ wkhtmltoimage 렌더링 실패: {e}")
            self._fallback_to_pil(html_content, output_path)

    def _render_with_chromium(self, html_content: str, output_path: str):
        """Chromium headless로 렌더링"""
        try:
            # 임시 HTML 파일 생성
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                temp_html = f.name

            # Chromium 명령 찾기
            chromium_cmd = None
            for cmd in ['chromium-browser', 'chromium', 'google-chrome']:
                try:
                    result = subprocess.run(['which', cmd], capture_output=True, text=True)
                    if result.returncode == 0:
                        chromium_cmd = cmd
                        break
                except:
                    continue

            if not chromium_cmd:
                raise Exception("Chromium을 찾을 수 없습니다")

            # Chromium headless 실행
            cmd = [
                chromium_cmd,
                '--headless',
                '--disable-gpu',
                '--screenshot=' + output_path,
                '--window-size=800,480',
                '--hide-scrollbars',
                'file://' + temp_html
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            # 임시 파일 삭제
            os.unlink(temp_html)

            if os.path.exists(output_path):
                print(f"✅ HTML 렌더링 완료: {output_path}")
            else:
                raise Exception("스크린샷 파일이 생성되지 않았습니다")

        except Exception as e:
            print(f"❌ Chromium 렌더링 실패: {e}")
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
