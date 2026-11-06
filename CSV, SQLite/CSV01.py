from pathlib import Path                    # 파일 경로 처리
import csv                                  # CSV 읽기·쓰기

CSV_PATH = Path("environment.csv")
new_file = not CSV_PATH.exists()            # 새 파일 여부

with CSV_PATH.open(
    "a", newline="", encoding="utf-8"       # 끝에 추가
) as file:
    writer = csv.writer(file)               # CSV 작성기

    if new_file:                            # 파일이 없었던 경우에만 헤더 작성
        writer.writerow([
            "timestamp", "temperature",
            "humidity", "status",
            "device_id", "error_message"
        ])