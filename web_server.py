#!/usr/bin/env python3
"""
Weather Dashboard Web UI
웹 브라우저를 통해 대시보드를 설정하고 관리할 수 있는 웹 인터페이스
"""

import os
import sys
import yaml
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv, set_key

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from src.weather_api import WeatherAPI
from src.display_generator import DisplayGenerator

# Flask 앱 초기화
app = Flask(__name__)
app.config['SECRET_KEY'] = 'weather-dashboard-secret-key'

# 전역 변수
dashboard_status = {
    "last_update": None,
    "status": "idle",
    "message": "",
    "current_weather": None
}

config_path = "config/config.inky.yaml"


def load_config():
    """설정 파일 로드"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config):
    """설정 파일 저장"""
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def update_weather_display():
    """날씨 디스플레이 업데이트 (백그라운드)"""
    global dashboard_status

    try:
        dashboard_status["status"] = "updating"
        dashboard_status["message"] = "날씨 정보를 가져오는 중..."

        # .env 로드
        load_dotenv()
        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            dashboard_status["status"] = "error"
            dashboard_status["message"] = "API 키가 설정되지 않았습니다."
            return

        # 설정 로드
        config = load_config()

        # Weather API
        weather_api = WeatherAPI(
            api_key=api_key,
            city=config["location"]["city"],
            country=config["location"]["country"]
        )

        # 현재 날씨
        current = weather_api.get_current_weather(
            lat=config["location"]["latitude"],
            lon=config["location"]["longitude"]
        )

        if not current:
            dashboard_status["status"] = "error"
            dashboard_status["message"] = "날씨 정보를 가져올 수 없습니다."
            return

        dashboard_status["current_weather"] = current

        # 사용자 정의 위치 이름 설정
        if "display_name" in config["location"]:
            current["display_name"] = config["location"]["display_name"]

        # 예보
        forecast = weather_api.get_forecast(
            lat=config["location"]["latitude"],
            lon=config["location"]["longitude"],
            hours=12
        )

        # 일별 예보
        daily_forecast = weather_api.get_daily_forecast(
            lat=config["location"]["latitude"],
            lon=config["location"]["longitude"],
            days=7
        )

        # 이미지 생성
        dashboard_status["message"] = "이미지 생성 중..."

        output_dir = Path(config["output"]["directory"])
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_{timestamp}.png"
        filepath = output_dir / filename

        # PIL 렌더러 사용 (InkyPi 스타일 디자인)
        generator = DisplayGenerator(
            width=config["display"]["width"],
            height=config["display"]["height"],
            color_mode=config["display"]["color_mode"]
        )
        generator.generate_weather_display(current, forecast, daily_forecast)
        generator.save(str(filepath))

        # 최신 이미지 링크 생성
        latest_link = output_dir / "latest.png"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(filepath.name)

        # 하드웨어 업데이트
        if config["display"]["mode"] == "hardware":
            dashboard_status["message"] = "하드웨어 디스플레이 업데이트 중..."
            try:
                from src.inky_display import InkyDisplay
                display = InkyDisplay()
                display.display_image(str(filepath))
            except Exception as e:
                print(f"하드웨어 업데이트 오류: {e}")

        dashboard_status["status"] = "success"
        dashboard_status["message"] = "업데이트 완료!"
        dashboard_status["last_update"] = datetime.now().isoformat()

    except Exception as e:
        dashboard_status["status"] = "error"
        dashboard_status["message"] = f"오류: {str(e)}"
        print(f"업데이트 오류: {e}")
        import traceback
        traceback.print_exc()


@app.route('/')
def index():
    """메인 페이지"""
    config = load_config()
    return render_template('index.html', config=config, status=dashboard_status)


@app.route('/settings')
def settings():
    """설정 페이지"""
    config = load_config()
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    return render_template('settings.html', config=config, api_key=api_key)


@app.route('/api/status')
def api_status():
    """상태 API"""
    return jsonify(dashboard_status)


@app.route('/api/update', methods=['POST'])
def api_update():
    """수동 업데이트 트리거"""
    thread = threading.Thread(target=update_weather_display)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started", "message": "업데이트를 시작했습니다."})


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """설정 API"""
    if request.method == 'GET':
        config = load_config()
        return jsonify(config)

    elif request.method == 'POST':
        try:
            data = request.json
            config = load_config()

            # 위치 업데이트
            if 'location' in data:
                config['location'].update(data['location'])

            # API 키 업데이트
            if 'api_key' in data:
                env_path = Path('.env')
                set_key(env_path, "OPENWEATHER_API_KEY", data['api_key'])

            # 설정 저장
            save_config(config)

            return jsonify({"status": "success", "message": "설정이 저장되었습니다."})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/preview')
def api_preview():
    """최신 이미지 미리보기"""
    output_dir = Path("output")
    latest_image = output_dir / "latest.png"

    if latest_image.exists():
        return send_from_directory(output_dir, "latest.png")
    else:
        # 가장 최근 이미지 찾기
        images = sorted(output_dir.glob("weather_*.png"))
        if images:
            return send_from_directory(output_dir, images[-1].name)

    return "이미지가 없습니다.", 404


@app.route('/output/<path:filename>')
def serve_output(filename):
    """출력 이미지 서빙"""
    return send_from_directory('output', filename)


def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("🌐 Weather Dashboard Web UI")
    print("=" * 60)
    print("\n브라우저에서 다음 주소로 접속하세요:")
    print("  http://raspberrypi.local:5000")
    print("  또는")
    print("  http://192.168.0.130:5000")
    print("\n종료하려면 Ctrl+C를 누르세요.")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
