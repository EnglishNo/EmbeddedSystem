import sqlite3                                          # Python 기본 SQLite 모듈

conn = sqlite3.connect("sensors.db")                    # DB 연결·생성

row = conn.execute("""
SELECT timestamp, temperature,
       humidity, status
FROM readings
ORDER BY timestamp DESC -- 시각 내림차순
LIMIT 1                 -- 한 건만 선택
""").fetchone()                                         # 튜플 한 건 또는 None

# 빈 테이블이면 출력하지 않음
if row is not None:
    timestamp, temperature, humidity, status = row
    print(timestamp, temperature, humidity, status)