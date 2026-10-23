import board                            # Raspberry Pi의 핀 이름 제공
import adafruit_dht                     # DHT 센서 드라이버

sensor = adafruit_dht.DHT22(            # 사용할 센서 모델 지정
    board.D17, use_pulseio=False        # BCM 17번, 비트뱅 방식
)

temperature = sensor.temperature        # 온도(섭씨) 읽기
humidity = sensor.humidity              # 상대습도(%RH) 읽기

print(f"온도: {temperature:.1f} ℃")     # 소수 첫째 자리로 표시
print(f"습도: {humidity:.1f} %RH")      # 값과 단위를 함께 출력

sensor.exit()                           # 정상 실행 경로의 센서 자원 정리
