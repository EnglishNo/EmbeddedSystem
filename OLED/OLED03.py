import board                                        # 보드의 SCL·SDA 핀 이름
import busio                                        # I²C 버스 인터페이스
import adafruit_ssd1306                             # OLED 드라이버

i2c = busio.I2C(board.SCL, board.SDA)               # 클록·데이터 핀 연결

# OLED 객체 생성
display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C                         # 가로·세로 픽셀 수, 버스, 주소
)

temperature = 25.4                                  # 화면 배치를 시험할 가상 온도
humidity = 61.2                                     # 화면 배치를 시험할 가상 습도

display.fill(0)                                     # 이전 화면 지우기

display.text("Temperature", 0, 0, 1)                # 온도 항목명
display.text(f"{temperature:.1f} C", 0, 16, 1)      # 온도와 단위

display.text("Humidity", 0, 34, 1)                  # 습도 항목명
display.text(f"{humidity:.1f} %RH", 0, 50, 1)       # 습도와 단위

display.show()                                      # 완성한 화면 전송