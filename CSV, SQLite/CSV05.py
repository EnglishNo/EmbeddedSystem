from pathlib import Path                    # 파일 경로 처리
import csv                                  # CSV 읽기·쓰기
from datetime import datetime               # 현재 날짜·시간 생성
from zoneinfo import ZoneInfo               # 타임존(Asia/Seoul) 처리
import time                                 # 주기적 측정을 위한 딜레이
import board                                # Raspberry Pi의 핀 이름 제공
import adafruit_dht                         # DHT 센서 드라이버

# 서울 타임존 설정 (Python 3.9+ 기본 지원)
KST = ZoneInfo("Asia/Seoul")

CSV_PATH = Path("environment.csv")          # 저장할 CSV 파일 경로

def init_csv():
    """CSV 파일이 없으면 헤더 행 생성"""
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", "temperature", "humidity",
                "status", "device_id", "error_message"
            ])

def append_csv(record):                     # 레코드 한 건을 추가하는 함수
    with CSV_PATH.open(
        "a", newline="", encoding="utf-8"   # 추가 모드(a)로 파일 열기
    ) as file:
        writer = csv.writer(file)

        # 헤더와 동일한 열 순서로 데이터 기록
        writer.writerow([
            record["timestamp"],            # 측정 일시
            record["temperature"],          # 온도 (None은 빈 칸으로 기록)
            record["humidity"],             # 습도 (None은 빈 칸으로 기록)
            record["status"],               # 상태 (정상 OK / 오류 ERROR)
            record["device_id"],            # 디바이스 식별자
            record["error_message"]         # 에러 사유
        ])

        file.flush()                        # Python 버퍼를 OS에 전달하여 즉시 디스크 반영

def validate(t, h):                         # 값 존재 여부와 허용 범위 검사
    if t is None or h is None:
        raise ValueError("missing value")   # 결측치 발생 시 예외
    if not (-40.0 <= t <= 80.0):
        raise ValueError("temperature range")  # 온도 허용 범위 초과
    if not (0.0 <= h <= 100.0):
        raise ValueError("humidity range")     # 습도 허용 범위 초과
    
    return round(t, 1), round(h, 1)         # 소수점 1자리로 반올림

def get_fresh_reading(max_retries=3, delay=1.5):
    """캐시 고정을 방지하기 위해 매 측정마다 인스턴스를 열고 닫는 함수"""
    last_error = ""
    for _ in range(max_retries):
        temp_sensor = None
        try:
            # 1. 센서 인스턴스를 매번 새로 생성하여 이전 드라이버 캐시를 완전히 날림
            temp_sensor = adafruit_dht.DHT22(board.D17, use_pulseio=False)
            
            # 2. 하드웨어에서 최신 온습도 펄스를 새로 읽어옴
            t_raw = temp_sensor.temperature
            h_raw = temp_sensor.humidity
            
            # 3. 유효성 검증
            t, h = validate(t_raw, h_raw)
            return t, h, "OK", ""
        except (RuntimeError, ValueError) as exc:
            last_error = str(exc)
            time.sleep(delay)               # 센서 안정화 및 재시도 간격
        finally:
            # 4. 읽기 시도 직후 GPIO 자원을 해제하여 캐시 잔류 방지
            if temp_sensor is not None:
                try:
                    temp_sensor.exit()
                except Exception:
                    pass

    # 모든 재시도 실패 시
    return None, None, "ERROR", last_error

# 최초 실행 시 CSV 헤더 확인 및 생성
init_csv()
print("5초 주기로 온습도 측정을 시작합니다. (종료: Ctrl + C)\n" + "-" * 50)

try:
    while True:
        # Asia/Seoul 기준 현재 시각 문자열 생성
        now_str = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

        # 캐시가 완전히 배제된 신선한 센서 데이터 수집
        t, h, status, error = get_fresh_reading(max_retries=3, delay=1.5)

        # CSV에 저장할 데이터 묶음
        record = {
            "timestamp": now_str,
            "temperature": t,
            "humidity": h,
            "status": status,
            "device_id": "PI_SENSOR_17",
            "error_message": error
        }

        # CSV 파일에 데이터 추가
        append_csv(record)

        # 터미널 콘솔에 진행 상황 실시간 출력
        if status == "OK":
            print(f"[{now_str}] 성공 -> 온도: {t}°C, 습도: {h}% (저장 완료)")
        else:
            print(f"[{now_str}] 실패 -> 상태: {status}, 원인: {error} (기록 완료)")

        # 5초 대기
        time.sleep(5)

except KeyboardInterrupt:
    print("\n측정을 안전하게 종료합니다.")