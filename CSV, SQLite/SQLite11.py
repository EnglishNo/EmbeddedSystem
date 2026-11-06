import csv                                          # CSV 파일 읽기/쓰기를 위한 파이썬 표준 라이브러리
from pathlib import Path                            # 파일 및 폴더 경로를 객체로 다루기 위한 모듈
import sqlite3                                      # SQLite 경량 데이터베이스를 다루는 모듈

# --- 1. 파일 경로 설정 ---
CSV_PATH = Path("environment.csv")                  # 데이터가 들어있는 원본 CSV 파일
DB_PATH = "sensors.db"                              # 데이터를 저장할 SQLite 데이터베이스 파일

# --- 2. DB 테이블 초기화 함수 (교재 23쪽) ---
def init_database(conn):
    """readings 테이블이 없으면 스키마에 맞춰 새로 생성"""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,       -- 고유 번호 (1씩 자동 증가)
        timestamp TEXT NOT NULL,                    -- 측정 일시 (문자열, 필수 입력)
        temperature REAL,                           -- 온도 수치 (에러 시 빈칸 -> NULL)
        humidity REAL,                              -- 습도 수치 (에러 시 빈칸 -> NULL)
        status TEXT NOT NULL,                       -- 수집 상태 ('OK' 또는 'ERROR')
        device_id TEXT NOT NULL,                    -- 라즈베리파이 센서 장치 ID
        error_message TEXT                          -- 에러 발생 원인 (정상이면 NULL)
    )
    """)
    conn.commit()                                   # 테이블 생성 확정 반영

# --- 3. SQL INSERT 템플릿 준비 (교재 24쪽) ---
INSERT_SQL = """
INSERT INTO readings (
    timestamp, temperature, humidity,
    status, device_id, error_message
) VALUES (?, ?, ?, ?, ?, ?)
"""                                                 # SQL Injection 방지를 위한 ? 플레이스홀더 사용

# --- 4. 단일 레코드 저장 함수 (교재 25쪽) ---
def insert_record(conn, record):
    """1개의 레코드를 트랜잭션(with 블록)으로 안전하게 DB에 저장"""
    try:
        with conn:                                  # 성공하면 commit, 예외 발생 시 자동으로 rollback
            conn.execute(INSERT_SQL, (
                record["timestamp"],
                record["temperature"],              # 실수(float) 또는 None (SQL의 NULL로 변환됨)
                record["humidity"],                 # 실수(float) 또는 None (SQL의 NULL로 변환됨)
                record["status"],
                record["device_id"],
                record["error_message"]             # 에러 내용 또는 None (SQL의 NULL로 변환됨)
            ))
    except sqlite3.Error as exc:
        print("DB 저장 실패:", exc)                 # 저장 중 에러가 나면 콘솔에 출력
        raise                                       # 호출한 쪽으로 에러를 다시 전달

# --- 5. CSV에서 SQLite로 데이터를 옮겨 담는 메인 함수 ---
def migrate_csv_to_sqlite():
    # 원본 파일이 있는지 먼저 확인
    if not CSV_PATH.exists():
        print(f"오류: {CSV_PATH} 파일이 현재 폴더에 존재하지 않습니다.")
        return

    conn = sqlite3.connect(DB_PATH)                 # DB 연결
    init_database(conn)                             # 테이블 생성 여부 확인

    inserted_count = 0                              # 저장 성공한 행 수 카운트 변수

    # DictReader로 헤더(열 이름)를 키로 삼아 한 줄씩 읽기 (교재 15쪽)
    with CSV_PATH.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # 빈 문자열("") 결측값 처리: 값이 있으면 float 변환, 비어있으면 None(SQL NULL) 처리
            t = float(row["temperature"]) if row["temperature"] else None
            h = float(row["humidity"]) if row["humidity"] else None
            err = row["error_message"] if row["error_message"] else None

            # DB에 넣을 형태에 맞춰 딕셔너리 생성
            record = {
                "timestamp": row["timestamp"],
                "temperature": t,
                "humidity": h,
                "status": row["status"],
                "device_id": row["device_id"],
                "error_message": err
            }

            insert_record(conn, record)             # DB에 1건 삽입
            inserted_count += 1                     # 카운트 증가

    conn.close()                                    # 모든 작업 후 DB 연결 종료

    # 콘솔에 완료 메시지 출력
    print("-" * 50)
    print(f"CSV 총 {inserted_count}개의 레코드가 SQLite({DB_PATH})에 성공적으로 저장되었습니다.")
    print("-" * 50)

# --- 실행 진입점 ---
if __name__ == "__main__":
    migrate_csv_to_sqlite()