import sqlite3                                          # Python 기본 SQLite 모듈
from pathlib import Path

conn = sqlite3.connect("sensors.db")                    # DB 연결·생성

# 실제로 DB에 저장된 날짜(2026-11-06)와 형식에 맞춘 범위 설정
day = "2026-11-06"
start_ts = f"{day} 00:00:00"                            # 시작 포함
end_ts   = "2026-11-07 00:00:00"                        # 끝 제외

# 1. 정상 데이터 통계 5개 값 조회
stats_ok = conn.execute("""
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

# 2. 같은 기간의 오류(ERROR) 건수 조회
error_count = conn.execute("""
SELECT COUNT(*)
FROM readings
WHERE status != 'OK'
  AND timestamp >= ?
  AND timestamp < ?
""", (start_ts, end_ts)).fetchone()[0]

# 3. 교재 스펙에 맞춰 6개 값(통계 5값 + 오류 건수)으로 결합
full_stats = (*stats_ok, error_count)

# --- [교재 본문 함수] ---
def build_report(day, stats):  # HTML 문자열 생성
    # 통계 다섯 값 + 같은 기간의 오류 건수
    avg_t, min_t, max_t, avg_h, count, errors = stats

    return f"""<!doctype html>
<html lang="ko"><meta charset="utf-8">
<title>{day} 센서 리포트</title>
<h1>{day} 센서 리포트</h1>
<ul>
  <li>평균 온도: {avg_t:.1f} °C</li>
  <li>최저/최고: {min_t:.1f} / {max_t:.1f} °C</li>
  <li>평균 습도: {avg_h:.1f} %</li>
  <li>정상 {count}건 · 오류 {errors}건</li>
</ul></html>"""  # .1f는 소수 한 자리 표시

# 4. 함수 호출 및 결과 생성
html_content = build_report(day, full_stats)

# 콘솔에 HTML 출력 확인
print(html_content)

# 파일로 저장하여 브라우저에서 열어볼 수 있도록 저장
Path("report.html").write_text(html_content, encoding="utf-8")
print("\n-> report.html 파일로 저장 완료!")