from pathlib import Path                    # 파일 경로 처리
import csv                                  # CSV 읽기·쓰기
from datetime import datetime               # 현재 날짜·시간 생성
import board                                # Raspberry Pi의 핀 이름 제공
import adafruit_dht                         # DHT 센서 드라이버

# 사용할 센서 모델 지정 (BCM 17번 핀, 비트뱅 방식)
sensor = adafruit_dht.DHT22(board.D17, use_pulseio=False)

CSV_PATH = Path("environment.csv")          # 저장할 CSV 파일 경로

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

        file.flush()                            # Python 버퍼를 OS에 전달하여 즉시 디스크 반영

def validate(t, h):                             # 값 존재 여부와 허용 범위 검사
    if t is None or h is None:
        raise ValueError("missing value")       # 결측치 발생 시 예외
    if not (-40.0 <= t <= 80.0):
        raise ValueError("temperature range")   # 온도 허용 범위 초과
    if not (0.0 <= h <= 100.0):
        raise ValueError("humidity range")      # 습도 허용 범위 초과
    
    return round(t, 1), round(h, 1)             # 소수점 1자리로 반올림

# 현재 시각 문자열 생성
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    t, h = validate(sensor.temperature, sensor.humidity)    # 센서 측정 및 유효성 검증
    status, error = "OK", ""                                # 정상 상태
except (RuntimeError, ValueError) as exc:
    t, h = None, None                                       # 실패 시 0이 아닌 None(빈 칸)으로 보관
    status, error = "ERROR", str(exc)                       # 오류 원인 보관
finally:
    sensor.exit()                                           # 정상/에러 무관하게 GPIO 자원 해제

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

# 터미널 콘솔에 최종 실행 결과 출력
if status == "OK":
    print(f"[{now_str}] 성공 -> 온도: {t}°C, 습도: {h}% (environment.csv 저장 완료)")
else:
    print(f"[{now_str}] 실패 -> 상태: {status}, 원인: {error} (environment.csv 저장 완료)")