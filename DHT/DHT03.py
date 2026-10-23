import board                                        # Raspberry Pi의 핀 이름 제공
import adafruit_dht                                 # DHT 센서 드라이버

sensor = adafruit_dht.DHT22(                        # 사용할 센서 모델 지정
    board.D17, use_pulseio=False                    # BCM 17번, 비트뱅 방식
)

success = failure = 0                               # 누적 집계 시 반복문 밖에서 초기화

# 한 번 측정하고 유효성 검사
try:
    t = sensor.temperature                          # 온도(℃)
    h = sensor.humidity                             # 상대습도(%RH)

    if t is None or h is None:                      # 값이 없는지 먼저 검사
        raise ValueError("값 없음")                  # 검증 실패로 분류
    
    if not (-40 <= t <= 80 and 0 <= h <= 100):      # 범위 검사
        raise ValueError("범위 초과")
    
    success += 1                                    # 모든 검사를 통과한 경우만 성공 집계

    print(f"정상 | {t:.1f} ℃ | {h:.1f} %RH")        # 정상 값 출력

# 센서 읽기 오류 처리
except RuntimeError as error:
    failure += 1                                    # 실패 횟수 증가
    print(f"재시도 | {error}")                       # 메시지 출력만 수행

# None 또는 범위 검사 실패
except ValueError as error:
    failure += 1
    print(f"제외 | {error}")                         # 정상 값으로 사용하지 않음
