import sqlite3                                  # Python 기본 SQLite 모듈
from datetime import datetime                   # 현재 날짜·시간 생성
from zoneinfo import ZoneInfo                   # 타임존(Asia/Seoul) 처리

# 1. DB 연결 및 테이블 생성 (테이블이 없을 때 발생하는 오류 방지)
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

# 2. 24쪽의 INSERT_SQL 정의 (재사용)
INSERT_SQL = """
INSERT INTO readings (
    timestamp, temperature, humidity,
    status, device_id, error_message
) VALUES (?, ?, ?, ?, ?, ?)
"""                                             # 여섯 값을 ? 위치에 바인딩

# 3. [교재 본문 코드] 한 건 저장 함수
def insert_record(conn, record):                # 한 건 저장 함수
    try:
        with conn:                              # 성공 시 commit, 예외 시 rollback
            conn.execute(INSERT_SQL, (
                record["timestamp"],
                record["temperature"],
                record["humidity"],
                record["status"],
                record["device_id"],
                record["error_message"]
            ))
    except sqlite3.Error as exc:                # DB 오류 처리
        print("DB 저장 실패:", exc)
        raise                                   # 호출한 쪽에도 오류 전달

# 4. 저장할 표본 데이터 준비 및 함수 호출 (정상 호출 테스트: 콘솔 출력 없이 1건 저장)
record = {
    "timestamp": datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
    "temperature": 25.0,
    "humidity": 50.0,
    "status": "OK",
    "device_id": "pi01",
    "error_message": None                       # None은 SQL NULL로 저장
}

insert_record(conn, record)                     # 함수 호출