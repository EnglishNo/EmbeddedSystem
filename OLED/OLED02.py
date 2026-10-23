import board                                # 보드의 SCL·SDA 핀 이름
import busio                                # I²C 버스 인터페이스
import adafruit_ssd1306                     # OLED 드라이버

i2c = busio.I2C(board.SCL, board.SDA)       # 클록·데이터 핀 연결

# OLED 객체 생성
display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C                 # 가로·세로 픽셀 수, 버스, 주소
)

# 먼저 I²C와 display를 초기화하고 글꼴 파일을 준비
display.fill(0)                             # 이전 화면의 픽셀을 버퍼에서 지움

display.text("Embedded System", 0, 0, 1)    # 첫 줄: 좌상단
display.text("I2C OLED",       0, 16, 1)    # 둘째 줄: y=16
display.text("Hello!",         0, 32, 1)    # 셋째 줄: y=32

display.show()                              # 세 줄을 그린 버퍼를 한 번에 전송