import csv                                          # CSV 파일 생성 모듈
from pathlib import Path                            # 파일 및 경로 제어 모듈
import sqlite3                                      # SQLite DB 제어 모듈

DB_PATH = "sensors.db"                              # 소스 DB 파일 경로
REPORT_DIR = Path("reports")                        # HTML 리포트 보관 디렉터리
REPORT_DIR.mkdir(exist_ok=True)                     # 리포트 폴더 생성 (이미 있으면 통과)

# 1. HTML 리포트 본문 생성 함수 (31쪽 기반)
def build_report(day, stats):
    """통계 5개 값과 오류 건수를 받아 HTML 문자열 반환"""
    avg_t, min_t, max_t, avg_h, count, errors = stats

    # 정상 데이터가 0건일 때 None 서식 오류(.1f) 방지
    avg_t = avg_t if avg_t is not None else 0.0
    min_t = min_t if min_t is not None else 0.0
    max_t = max_t if max_t is not None else 0.0
    avg_h = avg_h if avg_h is not None else 0.0

    return f"""<!doctype html>
<html lang="ko"><meta charset="utf-8">
<title>{day} 센서 리포트</title>
<h1>{day} 센서 리포트</h1>
<ul>
  <li>평균 온도: {avg_t:.1f} °C</li>
  <li>최저/최고: {min_t:.1f} / {max_t:.1f} °C</li>
  <li>평균 습도: {avg_h:.1f} %</li>
  <li>정상 {count}건 · 오류 {errors}건</li>
</ul></html>"""

# 2. 미션 C 통합 실행 함수 (HTML 생성 + CSV 내보내기 + 행 수 비교)
def generate_and_verify():
    conn = sqlite3.connect(DB_PATH)                 # DB 연결

    # 조회 대상 일자 및 시간 구간 정의
    day = "2026-11-06"
    start_ts = f"{day} 00:00:00"                    # 시작 시각 (이상, 포함)
    end_ts   = "2026-11-07 00:00:00"                # 종료 시각 (미만, 제외)

    # -------------------------------------------------------------
    # 1) 정상 통계 및 오류 수 집계 (28쪽 기반)
    # -------------------------------------------------------------
    stats_ok = conn.execute("""
    SELECT
        AVG(temperature),
        MIN(temperature),
        MAX(temperature),
        AVG(humidity),
        COUNT(*)
    FROM readings
    WHERE status = 'OK'
      AND timestamp >= ?
      AND timestamp < ?
    """, (start_ts, end_ts)).fetchone()

    error_count = conn.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE status != 'OK'
      AND timestamp >= ?
      AND timestamp < ?
    """, (start_ts, end_ts)).fetchone()[0]

    full_stats = (*stats_ok, error_count)           # 6개 튜플 구성
    db_ok_count = stats_ok[4]                       # DB 기준 정상 행 수

    # -------------------------------------------------------------
    # 2) HTML 리포트 생성 및 저장 (31~32쪽 기반)
    # -------------------------------------------------------------
    html_content = build_report(day, full_stats)
    report_file = REPORT_DIR / f"report_{day}.html"
    report_file.write_text(html_content, encoding="utf-8")
    print(f"[HTML 생성] {report_file.resolve()}")

    # -------------------------------------------------------------
    # 3) SQLite 정상 데이터 CSV 내보내기 (33쪽 기반)
    # -------------------------------------------------------------
    rows = conn.execute("""
    SELECT timestamp, temperature, humidity
    FROM readings
    WHERE status = 'OK'
      AND timestamp >= ?
      AND timestamp < ?
    ORDER BY timestamp ASC
    """, (start_ts, end_ts)).fetchall()

    export_csv_path = Path("daily_export.csv")
    with export_csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature", "humidity"])  # 헤더 1줄
        writer.writerows(rows)                                     # 데이터 일괄 쓰기

    print(f"[CSV 내보내기] {export_csv_path.resolve()}")

    # -------------------------------------------------------------
    # 4) 행 수 비교 및 검증 (33쪽, 42쪽 기반)
    # -------------------------------------------------------------
    # CSV 파일의 헤더를 제외한 실제 데이터 행 수 측정
    with export_csv_path.open("r", encoding="utf-8") as file:
        csv_lines = file.readlines()
        csv_data_count = max(0, len(csv_lines) - 1)  # 헤더(첫 줄) 제외

    print("\n" + "=" * 50)
    print("                [행 수 검증 결과]")
    print("=" * 50)
    print(f"  - DB 정상 데이터 수(COUNT) : {db_ok_count} 건")
    print(f"  - CSV 데이터 행 수(헤더 제외) : {csv_data_count} 건")

    if db_ok_count == csv_data_count:
        print("  -> 일치 여부: PASS (DB와 CSV 데이터 개수가 일치합니다.)")
    else:
        print("  -> 일치 여부: FAIL (수치가 불일치합니다. 확인 필요)")
    print("=" * 50)

    conn.close()

if __name__ == "__main__":
    generate_and_verify()