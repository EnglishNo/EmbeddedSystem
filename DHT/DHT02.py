import board                                    # Raspberry Pi의 핀 이름 제공
import adafruit_dht                             # DHT 센서 드라이버
import time                                     # 측정 사이 대기
from datetime import datetime                   # 측정 시각 기록

sensor = adafruit_dht.DHT22(                    # 사용할 센서 모델 지정
    board.D17, use_pulseio=False                # BCM 17번, 비트뱅 방식
)

# sensor 초기화 후 실행하며, exit()는 반복 종료 뒤에 배치
for count in range(1, 11):                      # 1부터 10까지 총 10회
    temperature = sensor.temperature            # 온도 읽기
    humidity = sensor.humidity                  # 습도 읽기

    now = datetime.now().strftime("%H:%M:%S")   # 시:분:초

    print(f"{count:02d} {now} | "               # 순번을 01~10으로 표시
          f"{temperature:.1f} ℃ | "            # 소수 첫째 자리 온도
          f"{humidity:.1f} %RH")                # 습도와 단위
    
    time.sleep(2.0)                             # 처리 후 2초 기다리고 다음 측정