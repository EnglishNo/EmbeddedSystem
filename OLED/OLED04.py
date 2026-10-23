import time                                             # 반복 측정 사이 대기
import board                                            # GPIO·I²C 핀 이름
import busio                                            # I²C 버스 객체
import adafruit_dht                                     # 5주차 DHT 드라이버 필요
import adafruit_ssd1306                                 # OLED 드라이버

# DHT22 입력 객체
sensor = adafruit_dht.DHT22(
    board.D17, use_pulseio=False                        # DATA는 BCM GPIO17
)

# OLED용 I²C 버스
i2c = busio.I2C(board.SCL, board.SDA)

# OLED 출력 객체
display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C                             # 실제 해상도·주소와 일치
)

# 바깥 try: 반복 종료 시 finally로 이동
try:
    # 측정·검증·표시 반복
    while True:
        # 안쪽 try: 한 회차의 오류 처리
        try:
            t = sensor.temperature                      # 온도 읽기
            h = sensor.humidity                         # 습도 읽기

            if t is None or h is None:                  # 값 없음 검사
                raise ValueError("No value")
            
            if not (-40 <= t <= 80 and 0 <= h <= 100):  # 범위 검사
                raise ValueError("Out of range")
            
            display.fill(0)  # 정상 화면 준비

            display.text(f"T: {t:.1f} C", 0, 8, 1)      # 온도 표시
            display.text(f"H: {h:.1f} %RH", 0, 32, 1)   # 습도 표시
        # 두 예외 처리
        except (RuntimeError, ValueError) as error:
            display.fill(0)  # 이전 정상 값을 지움

            display.text("Sensor Error", 0, 8, 1)       # 오류 안내
            display.text(str(error)[:20], 0, 32, 1)     # 앞 20자

        # 정상·오류 중 준비한 화면 전송
        display.show()

        # 2초 대기 뒤 다음 회차
        time.sleep(2.0)
# Ctrl+C 등으로 반복 종료 시 실행
finally:
    display.fill(0); display.show(); sensor.exit()      # 화면 지우기·센서 정리