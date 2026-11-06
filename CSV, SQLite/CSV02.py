from pathlib import Path                    # 파일 경로 처리
import csv                                  # CSV 읽기·쓰기

CSV_PATH = Path("environment.csv")

def append_csv(record):                     # 레코드 한 건을 추가
    with CSV_PATH.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        # 헤더와 동일한 열 순서
        writer.writerow([
            record["timestamp"],
            record["temperature"],          # None은 빈 칸
            record["humidity"],
            record["status"],               # 정상 OK / 오류 ERROR
            record["device_id"],
            record["error_message"]
        ])

        file.flush()                        # Python 버퍼를 OS에 전달

from datetime import datetime

# # 1. 정상 데이터 기록 예시
# data_ok = {
#     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     "temperature": 23.5,
#     "humidity": 45.2,
#     "status": "OK",
#     "device_id": "SENSOR_01",
#     "error_message": ""                     # 에러가 없을 때는 빈 문자열 전달
# }

# append_csv(data_ok)


# 2. 에러 발생 시 기록 예시 (온/습도 측정 불가 시)
data_error = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "temperature": None,                        # None을 넣으면 CSV에 빈 칸으로 기록됨
    "humidity": None,
    "status": "ERROR",
    "device_id": "SENSOR_01",
    "error_message": "Sensor read timeout"
}

append_csv(data_error)