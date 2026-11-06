from pathlib import Path                                # 파일 경로 처리
import csv

CSV_PATH = Path("environment.csv")

with CSV_PATH.open(
    "r", newline="", encoding="utf-8"                   # 읽기 모드
) as file:
    reader = csv.DictReader(file)                       # 헤더를 키로 사용

    for row in reader:                                  # 레코드마다 반복
        if row["status"] != "OK":
            continue                                    # 오류 행은 건너뜀

        temperature = float(row["temperature"])
        humidity = float(row["humidity"])               # 수치 변환

        print(row["timestamp"], temperature, humidity)