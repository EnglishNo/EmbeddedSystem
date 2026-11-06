import sqlite3                                          # Python 기본 SQLite 모듈

conn = sqlite3.connect("sensors.db")                    # DB 연결·생성

conn.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 고유 번호
    timestamp TEXT NOT NULL,                -- 측정 시각: 필수
    temperature REAL,                       -- 온도: NULL 허용
    humidity REAL,                          -- 습도: NULL 허용
    status TEXT NOT NULL,                   -- 정상·오류 상태
    device_id TEXT NOT NULL,                -- 장치 식별자
    error_message TEXT                      -- 오류 원인
)
""")

conn.commit()                                           # 변경 사항 확정