import threading
from queue import Queue
import sqlite3                                  # Python 기본 SQLite 모듈
from datetime import datetime                   # 측정 시각 생성
from zoneinfo import ZoneInfo                   # 타임존(Asia/Seoul) 처리

KST = ZoneInfo("Asia/Seoul")

# 1. 24쪽의 INSERT_SQL 정의
INSERT_SQL = """
INSERT INTO readings (
    timestamp, temperature, humidity,
    status, device_id, error_message
) VALUES (?, ?, ?, ?, ?, ?)
"""

# 2. 23쪽의 테이블 생성을 함수로 준비
def create_table(conn):
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
    conn.commit()

# 3. 25쪽의 한 건 저장 함수
def insert_record(conn, record):
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

# --- [35쪽 교재 본문] ---
records = Queue(maxsize=200)                    # 대기 레코드 최대 200개

def db_writer():
    conn = sqlite3.connect("sensors.db")        # 이 스레드의 연결
    create_table(conn)                          # 23쪽 테이블 생성을 함수로 준비
    try:
        while True:
            record = records.get()              # 항목이 올 때까지 대기
            try:
                if record is None:              # 종료 신호
                    break
                insert_record(conn, record)     # 25쪽 함수
            finally:
                records.task_done()             # 처리 완료 통지
    finally:
        conn.close()                            # 연결 자원 해제

# --- 동작 검증을 위한 실행 흐름 (교재 35쪽 예상 동작 기준) ---
if __name__ == "__main__":
    # 1. DB 저장 전용 스레드 시작
    writer_thread = threading.Thread(target=db_writer)
    writer_thread.start()

    # 2. 생산자: Queue에 테스트 레코드 투입
    sample_record = {
        "timestamp": datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": 25.0,
        "humidity": 50.0,
        "status": "OK",
        "device_id": "PI_SENSOR_17",
        "error_message": None
    }
    records.put(sample_record)

    # 3. 모든 생산자 종료 후 안전 종료 신호 전달
    records.put(None)                           # 기존 레코드 뒤에 종료 신호 추가

    # 4. 큐가 모두 비워지고 스레드가 끝날 때까지 대기
    records.join()
    writer_thread.join()
    print("DB 저장 스레드가 안전하게 종료되었습니다.")