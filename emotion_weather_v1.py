import json
import random
from datetime import datetime

class EmotionWeather:
    def __init__(self):
        self.weather_map = {
            "CLEAR": "☀️ 맑음 (최상: 모든 시스템 정상, 베팅 공격성 강화)",
            "CLOUDY": "☁️ 흐림 (주의: 지연 시간 발생, 데이터 노이즈 감지)",
            "THUNDER": "⚡ 천둥 (위험: API 에러 발생, 생존 모드 전환 필요)",
            "RAIN": "🌧️ 비 (우울: 수익률 저하, 로직 재검토 중)",
            "RAINBOW": "🌈 무지개 (축제: 목표 수익 달성, 서비스 고도화 가동)"
        }

    def analyze_status(self, success_rate, api_errors, pnl):
        if api_errors > 3:
            return "THUNDER"
        if pnl > 0.1: # 10% profit
            return "RAINBOW"
        if success_rate > 0.8:
            return "CLEAR"
        if pnl < -0.05:
            return "RAIN"
        return "CLOUDY"

    def get_weather_report(self, success_rate, api_errors, pnl):
        state = self.analyze_status(success_rate, api_errors, pnl)
        weather_desc = self.weather_map[state]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": state,
            "description": weather_desc,
            "metrics": {
                "success_rate": success_rate,
                "api_errors": api_errors,
                "pnl": f"{pnl*100}%"
            }
        }
        return report

if __name__ == "__main__":
    # 시뮬레이션: 현재 $6 생존 챌린지 돌입 전 '전운'이 감도는 상황
    ew = EmotionWeather()
    state = ew.get_weather_report(success_rate=0.95, api_errors=0, pnl=0.0) # 평온한 상태
    print(json.dumps(state, indent=2, ensure_ascii=False))
