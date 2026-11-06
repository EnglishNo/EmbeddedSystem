import sqlite3                                          # SQLite 데이터베이스 제어 라이브러리
from pathlib import Path                                # 객체 지향적 파일 및 디렉터리 경로 처리

# 1. 데이터베이스 연결
conn = sqlite3.connect("sensors.db")                    # 센서 데이터가 저장된 DB 파일 열기

# 2. 리포트 저장용 디렉터리 준비
REPORT_DIR = Path("reports")                            # 리포트를 모아둘 'reports' 폴더 경로 지정
REPORT_DIR.mkdir(exist_ok=True)                         # 폴더가 없으면 새로 생성 (이미 있어도 에러 안 남)

# 3. 조회할 날짜 및 시간 범위 설정
day = "2026-11-06"                                      # 리포트를 생성할 기준 일자
start_ts = f"{day} 00:00:00"                            # 해당 날짜의 시작 시각 (이상, 포함)
end_ts   = "2026-11-07 00:00:00"                        # 다음 날의 자정 시각 (미만, 제외)

# 4. 해당 일자의 정상('OK') 데이터 통계 5개 값 추출
stats_ok = conn.execute("""
SELECT
    AVG(temperature),                                  -- 평균 온도 계산
    MIN(temperature),                                  -- 최저 온도 계산
    MAX(temperature),                                  -- 최고 온도 계산
    AVG(humidity),                                     -- 평균 습도 계산
    COUNT(*)                                           -- 정상 수집된 총 행 수
FROM readings
WHERE status = 'OK'                                     -- 오류 행은 제외하고 정상 데이터만 필터링
  AND timestamp >= ?                                   -- 조회 시작 시각 이상
  AND timestamp < ?                                    -- 조회 종료 시각 미만
""", (start_ts, end_ts)).fetchone()                    # 단일 행 결과(튜플) 가져오기

# 5. 해당 일자의 오류('ERROR') 건수 추출
error_count = conn.execute("""
SELECT COUNT(*)                                        -- 오류 발생 총 건수 계산
FROM readings
WHERE status != 'OK'                                    -- OK가 아닌 모든 상태 필터링
  AND timestamp >= ?                                   -- 조회 시작 시각 이상
  AND timestamp < ?                                    -- 조회 종료 시각 미만
""", (start_ts, end_ts)).fetchone()[0]                 # 첫 번째 열 값(정수 숫자)만 추출

# 6. 교재 스펙(6개 묶음)에 맞춰 통계 5개와 오류 건수 1개를 결합
full_stats = (*stats_ok, error_count)

# 7. HTML 문서 생성 함수 정의
def build_report(day, stats):
    # 6개 튜플 값을 개별 변수로 언패킹
    avg_t, min_t, max_t, avg_h, count, errors = stats

    # 정상 데이터가 0건일 경우 None 서식 오류(:.1f)를 방지하는 기본값 방어 코드
    avg_t = avg_t if avg_t is not None else 0.0
    min_t = min_t if min_t is not None else 0.0
    max_t = max_t if max_t is not None else 0.0
    avg_h = avg_h if avg_h is not None else 0.0

    # 브라우저에 표시될 HTML 문자열 서식 완성
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

# 8. HTML 본문 생성
html_content = build_report(day, full_stats)

# 9. 날짜별 파일 경로 지정 (reports/report_2026-11-06.html)
report_path = REPORT_DIR / f"report_{day}.html"

# 10. 파일 쓰기 및 저장 (동일 날짜 재실행 시 최신 내용으로 덮어씀)
report_path.write_text(html_content, encoding="utf-8")

# 11. 최종 생성된 파일의 시스템 절대 경로 콘솔 출력
print("생성:", report_path.resolve())