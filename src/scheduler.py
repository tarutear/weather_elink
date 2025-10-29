"""
날씨 대시보드 자동 업데이트 스케줄러
"""

import schedule
import time
from datetime import datetime
from typing import Callable
import signal
import sys


class WeatherScheduler:
    """날씨 업데이트 스케줄러"""

    def __init__(self, update_func: Callable, interval_seconds: int = 3600):
        """
        스케줄러 초기화

        Args:
            update_func: 실행할 업데이트 함수
            interval_seconds: 업데이트 간격 (초) - 기본값: 3600 (1시간)
        """
        self.update_func = update_func
        self.interval_seconds = interval_seconds
        self.is_running = False

        # 우아한 종료를 위한 시그널 핸들러
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """시그널 핸들러 (Ctrl+C 등)"""
        print("\n\n⏹  스케줄러를 종료합니다...")
        self.is_running = False
        sys.exit(0)

    def run_once(self):
        """한 번만 실행"""
        print(f"🔄 날씨 정보 업데이트 중... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        try:
            self.update_func()
            print("✅ 업데이트 완료!")
        except Exception as e:
            print(f"❌ 업데이트 실패: {e}")

    def start(self, run_immediately: bool = True):
        """
        스케줄러 시작

        Args:
            run_immediately: 즉시 한 번 실행할지 여부
        """
        print("=" * 60)
        print("🌤  날씨 E-ink 대시보드 스케줄러 시작")
        print("=" * 60)
        print(f"📅 업데이트 간격: {self.interval_seconds}초 ({self.interval_seconds // 60}분)")
        print(f"⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n종료하려면 Ctrl+C를 누르세요.\n")

        # 즉시 실행
        if run_immediately:
            self.run_once()

        # 스케줄 등록
        schedule.every(self.interval_seconds).seconds.do(self.run_once)

        # 무한 루프
        self.is_running = True
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

    def start_daemon(self):
        """백그라운드 데몬으로 실행"""
        print("🔧 데몬 모드는 systemd 서비스로 구현하는 것을 권장합니다.")
        print("systemd 서비스 예제는 README.md를 참고하세요.")
        self.start()


def test_scheduler():
    """스케줄러 테스트"""

    def dummy_update():
        print(f"  → 더미 업데이트 실행: {datetime.now()}")

    # 10초마다 업데이트하는 테스트 스케줄러
    scheduler = WeatherScheduler(dummy_update, interval_seconds=10)
    scheduler.start()


if __name__ == "__main__":
    test_scheduler()
