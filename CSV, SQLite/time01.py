from datetime import datetime                # 현재 날짜·시간
from zoneinfo import ZoneInfo               # 지역별 시간대

KST = ZoneInfo("Asia/Seoul")                # 한국 표준시
def now_text():
# 시간대가 포함된 ISO 8601 문자열을 반환
    return datetime.now(KST).isoformat(
        timespec="seconds"                  # 소수 초를 생략
    )

print(now_text())                           # 실행 시점의 시간을 출력