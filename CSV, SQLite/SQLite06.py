import sqlite3                                          # Python 기본 SQLite 모듈

conn = sqlite3.connect("sensors.db")                    # DB 연결·생성

# 실제로 DB에 저장된 날짜(2026-11-06)와 형식에 맞춘 범위 설정
start_ts = "2026-11-06 00:00:00"                        # 시작 포함
end_ts   = "2026-11-07 00:00:00"                        # 끝 제외

stats = conn.execute("""
SELECT
    AVG(temperature), -- 평균 온도
    MIN(temperature), -- 최저 온도
    MAX(temperature), -- 최고 온도
    AVG(humidity),    -- 평균 습도
    COUNT(*)          -- 정상 행 수
FROM readings
WHERE status = 'OK'
  AND timestamp >= ?
  AND timestamp < ?
""", (start_ts, end_ts)).fetchone()

avg_t, min_t, max_t, avg_h, count = stats  # 다섯 값
print("순서대로 평균 온도 / 최저 온도 / 최고 온도 / 평균 습도 / 정상 행 수")
print(stats)