import sqlite3                                          # SQLite 데이터베이스 연동 모듈

DB_PATH = "sensors.db"                                  # 조회할 데이터베이스 파일 경로

def query_sensor_data():
    conn = sqlite3.connect(DB_PATH)                     # 데이터베이스 연결

    print("=" * 60)
    print("         SQLite 센서 데이터 조회 및 통계 리포트")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 최신 기록 1건 조회 (26쪽 기반)
    # -------------------------------------------------------------
    # ORDER BY timestamp DESC LIMIT 1을 사용해 가장 최근 수집된 행 선택
    latest_row = conn.execute("""
    SELECT timestamp, temperature, humidity, status, device_id, error_message
    FROM readings
    ORDER BY timestamp DESC
    LIMIT 1
    """).fetchone()

    print("\n[1. 최신 데이터 1건 조회]")
    if latest_row:
        ts, temp, hum, status, dev, err = latest_row
        print(f"  - 시각: {ts}")
        print(f"  - 상태: {status} (장치: {dev})")
        print(f"  - 온도: {temp} °C" if temp is not None else "  - 온도: None (결측)")
        print(f"  - 습도: {hum} %" if hum is not None else "  - 습도: None (결측)")
        if err:
            print(f"  - 오류 메시지: {err}")
    else:
        print("  데이터가 비어 있습니다.")

    # -------------------------------------------------------------
    # 2. 오늘(지정 일자) 기간 범위 설정 및 정상 데이터 목록 조회 (27쪽 기반)
    # -------------------------------------------------------------
    # [시작 포함, 끝 제외) 구간으로 날짜 중복 없이 조회
    day = "2026-11-06"
    start_ts = f"{day} 00:00:00"                        # 시작 시각 이상
    end_ts   = "2026-11-07 00:00:00"                    # 익일 자정 미만

    # WHERE status = 'OK' 조건으로 정상 데이터만 필터링하여 시간순 정렬
    period_rows = conn.execute("""
    SELECT timestamp, temperature, humidity
    FROM readings
    WHERE status = 'OK'
      AND timestamp >= ?
      AND timestamp < ?
    ORDER BY timestamp ASC
    """, (start_ts, end_ts)).fetchall()

    print(f"\n[2. 오늘({day}) 기간 정상 데이터 목록]")
    print(f"  - 정상 수집 건수: {len(period_rows)}건")
    print("  - 표본 데이터 (앞 3건):")
    for r in period_rows[:3]:
        print(f"    {r[0]} -> 온도: {r[1]}°C, 습도: {r[2]}%")
    if len(period_rows) > 3:
        print(f"    ... 외 {len(period_rows) - 3}건 생략 ...")

    # -------------------------------------------------------------
    # 3. SQL 집계 함수를 통한 통계 요약 (28쪽 기반)
    # -------------------------------------------------------------
    # AVG, MIN, MAX, COUNT(*)를 사용해 DB 엔진에서 직접 계산 (NULL 제외 집계)
    stats_ok = conn.execute("""
    SELECT
        AVG(temperature),                               -- 평균 온도
        MIN(temperature),                               -- 최저 온도
        MAX(temperature),                               -- 최고 온도
        AVG(humidity),                                  -- 평균 습도
        COUNT(*)                                        -- 정상 측정 행 수
    FROM readings
    WHERE status = 'OK'
      AND timestamp >= ?
      AND timestamp < ?
    """, (start_ts, end_ts)).fetchone()

    # 같은 기간 동안 발생한 오류(ERROR) 건수 조회
    error_count = conn.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE status != 'OK'
      AND timestamp >= ?
      AND timestamp < ?
    """, (start_ts, end_ts)).fetchone()[0]

    avg_t, min_t, max_t, avg_h, ok_count = stats_ok

    print(f"\n[3. 오늘({day}) 통계 요약]")
    if ok_count > 0:
        print(f"  - 평균 온도 : {avg_t:.1f} °C")
        print(f"  - 최저 온도 : {min_t:.1f} °C")
        print(f"  - 최고 온도 : {max_t:.1f} °C")
        print(f"  - 평균 습도 : {avg_h:.1f} %")
        print(f"  - 수집 집계 : 정상 {ok_count}건 / 오류 {error_count}건 (총 {ok_count + error_count}건)")
    else:
        print("  조회 기간 내 정상 데이터가 존재하지 않습니다.")

    conn.close()                                        # DB 연결 해제
    print("=" * 60)

if __name__ == "__main__":
    query_sensor_data()