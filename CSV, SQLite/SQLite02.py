import sqlite3                                  # Python 기본 SQLite 모듈
from datetime import datetime                   # 현재 날짜·시간 생성
from zoneinfo import ZoneInfo                   # 타임존(Asia/Seoul) 처리

# 1. 23쪽에 정의되어 있어야 하는 DB 연결 및 테이블 생성
conn = sqlite3.connect("sensors.db")            # DB 연결·생성
conn.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    temperature REAL,
    humidity REAL,
    status TEXT NOT NULL,
    device_id TEXT NOT NULL,
    error_message TEXT
)
""")
conn.commit()

# 2. 23쪽에 정의되어 있어야 하는 record 데이터 (교재 표본 데이터 기준)
record = {
    "timestamp": datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
    "temperature": 25.0,
    "humidity": 50.0,
    "status": "OK",
    "device_id": "pi01",
    "error_message": None                       # None은 DB에 NULL로 저장됨
}

# 3. [교재 본문 코드]
INSERT_SQL = """
INSERT INTO readings (
    timestamp, temperature, humidity,
    status, device_id, error_message
) VALUES (?, ?, ?, ?, ?, ?)
""" # 여섯 값을 ? 위치에 바인딩

values = ( # INSERT의 열 순서와 동일하게 구성
    record["timestamp"], record["temperature"],
    record["humidity"], record["status"],
    record["device_id"], record["error_message"]
)

conn.execute(INSERT_SQL, values) # 한 행 삽입
conn.commit() # 저장 확정