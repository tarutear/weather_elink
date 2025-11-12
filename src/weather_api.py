"""
날씨 API 연동 모듈
OpenWeatherMap API를 사용하여 한국 날씨 정보를 가져옵니다.
"""

import requests
import os
from datetime import datetime
from typing import Dict, List, Optional
import json


class WeatherAPI:
    """날씨 API 클래스"""

    def __init__(self, api_key: str, city: str = "Seoul", country: str = "KR"):
        """
        WeatherAPI 초기화

        Args:
            api_key: OpenWeatherMap API 키
            city: 도시명 (기본값: Seoul)
            country: 국가 코드 (기본값: KR)
        """
        self.api_key = api_key
        self.city = city
        self.country = country
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, lat: Optional[float] = None, lon: Optional[float] = None) -> Dict:
        """
        현재 날씨 정보 가져오기

        Args:
            lat: 위도 (옵션)
            lon: 경도 (옵션)

        Returns:
            현재 날씨 정보 딕셔너리
        """
        endpoint = f"{self.base_url}/weather"

        params = {
            "appid": self.api_key,
            "units": "metric",  # 섭씨 온도
            "lang": "kr"  # 한국어 설명
        }

        if lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        else:
            params["q"] = f"{self.city},{self.country}"

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._parse_current_weather(data)

        except requests.exceptions.RequestException as e:
            print(f"날씨 정보 가져오기 실패: {e}")
            return {}

    def get_forecast(self, lat: Optional[float] = None, lon: Optional[float] = None,
                     hours: int = 12) -> List[Dict]:
        """
        시간별 예보 정보 가져오기

        Args:
            lat: 위도 (옵션)
            lon: 경도 (옵션)
            hours: 예보 시간 (기본값: 12시간)

        Returns:
            예보 정보 리스트
        """
        endpoint = f"{self.base_url}/forecast"

        params = {
            "appid": self.api_key,
            "units": "metric",
            "lang": "kr"
        }

        if lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        else:
            params["q"] = f"{self.city},{self.country}"

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._parse_forecast(data, hours)

        except requests.exceptions.RequestException as e:
            print(f"예보 정보 가져오기 실패: {e}")
            return []

    def get_daily_forecast(self, lat: Optional[float] = None, lon: Optional[float] = None,
                           days: int = 7) -> List[Dict]:
        """
        일별 예보 정보 가져오기 (최대 7일)

        Args:
            lat: 위도 (옵션)
            lon: 경도 (옵션)
            days: 예보 일수 (기본값: 7일)

        Returns:
            일별 예보 정보 리스트
        """
        endpoint = f"{self.base_url}/forecast"

        params = {
            "appid": self.api_key,
            "units": "metric",
            "lang": "kr"
        }

        if lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        else:
            params["q"] = f"{self.city},{self.country}"

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._parse_daily_forecast(data, days)

        except requests.exceptions.RequestException as e:
            print(f"일별 예보 정보 가져오기 실패: {e}")
            return []

    def _parse_current_weather(self, data: Dict) -> Dict:
        """현재 날씨 데이터 파싱"""
        if not data:
            return {}

        # 가시거리를 km로 변환 (API는 미터 단위)
        visibility_m = data.get("visibility", 10000)
        visibility_km = round(visibility_m / 1000, 1)

        return {
            "timestamp": datetime.now().isoformat(),
            "location": data.get("name", ""),
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "temp_min": round(data["main"]["temp_min"], 1),
            "temp_max": round(data["main"]["temp_max"], 1),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather_main": data["weather"][0]["main"],
            "weather_description": data["weather"][0]["description"],
            "weather_icon": data["weather"][0]["icon"],
            "wind_speed": round(data["wind"]["speed"], 1),
            "wind_deg": data["wind"].get("deg", 0),
            "clouds": data["clouds"]["all"],
            "visibility": visibility_km,
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
        }

    def _parse_forecast(self, data: Dict, hours: int) -> List[Dict]:
        """예보 데이터 파싱"""
        if not data or "list" not in data:
            return []

        forecasts = []
        # OpenWeatherMap은 3시간 간격으로 예보 제공
        count = min(hours // 3 + 1, len(data["list"]))

        for item in data["list"][:count]:
            forecasts.append({
                "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                "datetime": datetime.fromtimestamp(item["dt"]).isoformat(),
                "temperature": round(item["main"]["temp"], 1),
                "weather_main": item["weather"][0]["main"],
                "weather_description": item["weather"][0]["description"],
                "weather_icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
                "wind_speed": round(item["wind"]["speed"], 1),
                "pop": int(item.get("pop", 0) * 100),  # 강수 확률 (%)
            })

        return forecasts

    def _parse_daily_forecast(self, data: Dict, days: int) -> List[Dict]:
        """일별 예보 데이터 파싱 (3시간 간격 데이터를 일별로 그룹화)"""
        if not data or "list" not in data:
            return []

        # 날짜별로 데이터 그룹화
        daily_data = {}
        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")

            if date_key not in daily_data:
                daily_data[date_key] = {
                    "date": dt,
                    "temps": [],
                    "weather_icons": [],
                    "weather_mains": [],
                    "descriptions": []
                }

            daily_data[date_key]["temps"].append(item["main"]["temp"])
            daily_data[date_key]["weather_icons"].append(item["weather"][0]["icon"])
            daily_data[date_key]["weather_mains"].append(item["weather"][0]["main"])
            daily_data[date_key]["descriptions"].append(item["weather"][0]["description"])

        # 일별 요약 생성
        daily_forecasts = []
        for date_key in sorted(daily_data.keys())[:days]:
            day_data = daily_data[date_key]
            dt = day_data["date"]

            # 가장 빈번한 날씨 상태 선택 (낮 시간대 우선)
            midday_icons = [icon for icon in day_data["weather_icons"] if icon.endswith('d')]
            representative_icon = midday_icons[len(midday_icons)//2] if midday_icons else day_data["weather_icons"][0]

            daily_forecasts.append({
                "date": dt.strftime("%Y-%m-%d"),
                "day_name": dt.strftime("%a"),  # Mon, Tue, Wed...
                "day_name_kr": ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()],
                "temp_max": round(max(day_data["temps"]), 1),
                "temp_min": round(min(day_data["temps"]), 1),
                "weather_icon": representative_icon,
                "weather_main": day_data["weather_mains"][0],
                "weather_description": day_data["descriptions"][0]
            })

        return daily_forecasts

    def get_weather_icon_code(self, icon: str) -> str:
        """
        OpenWeatherMap 아이콘 코드를 간단한 문자열로 변환

        Args:
            icon: OpenWeatherMap 아이콘 코드 (예: '01d', '10n')

        Returns:
            간단한 날씨 코드 (예: 'clear', 'rain', 'cloud')
        """
        icon_map = {
            "01": "clear",      # 맑음
            "02": "few_clouds", # 구름 조금
            "03": "clouds",     # 구름 많음
            "04": "clouds",     # 흐림
            "09": "rain",       # 소나기
            "10": "rain",       # 비
            "11": "thunder",    # 천둥번개
            "13": "snow",       # 눈
            "50": "mist",       # 안개
        }

        code = icon[:2]
        return icon_map.get(code, "unknown")


def test_weather_api():
    """API 테스트 함수"""
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("❌ OPENWEATHER_API_KEY가 .env 파일에 설정되어 있지 않습니다.")
        print("\n.env 파일을 생성하고 다음을 추가하세요:")
        print("OPENWEATHER_API_KEY=your_api_key_here")
        print("\nAPI 키는 https://openweathermap.org/api 에서 무료로 발급받을 수 있습니다.")
        return

    weather = WeatherAPI(api_key, city="Seoul", country="KR")

    print("=== 현재 날씨 ===")
    current = weather.get_current_weather()
    if current:
        print(f"위치: {current['location']}")
        print(f"온도: {current['temperature']}°C (체감: {current['feels_like']}°C)")
        print(f"날씨: {current['weather_description']}")
        print(f"습도: {current['humidity']}%")
        print(f"풍속: {current['wind_speed']} m/s")
        print(f"일출: {current['sunrise']} / 일몰: {current['sunset']}")

    print("\n=== 12시간 예보 ===")
    forecast = weather.get_forecast(hours=12)
    for f in forecast:
        print(f"{f['time']} - {f['temperature']}°C, {f['weather_description']} (강수확률: {f['pop']}%)")


if __name__ == "__main__":
    test_weather_api()
