import board                                    # 보드의 SCL·SDA 핀 이름
import busio                                    # I²C 버스 인터페이스
import adafruit_ssd1306                         # OLED 드라이버
from smbus2 import SMBus                        # I²C 버스를 직접 제어하는 라이브러리

i2c = busio.I2C(board.SCL, board.SDA)           # 클록·데이터 핀 연결

# OLED 객체 생성
display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C                     # 가로·세로 픽셀 수, I²C 버스, OLED 주소
)

# I²C 버스 1번 사용
bus = SMBus(1)                                  # 라즈베리 파이의 I²C 버스 1번 열기
I2CAddress = ""                                 # 검색한 I²C 주소를 저장할 문자열 변수

# 연결된 장치의 주소 검색
for address in range(0x03, 0x78):               # 사용 가능한 I²C 주소 범위를 순회
    try:
        bus.read_byte(address)                  # 해당 주소의 장치에 읽기 요청을 보내 응답 확인
        print(f"I2C 장치 발견: 0x{address:02X}") # 발견한 장치의 주소를 16진수 대문자로 출력
        I2CAddress = f"0x{address:02X}"         # 검색한 주소를 문자열로 변환하여 변수에 저장
    except OSError:
        pass                                    # 장치가 응답하지 않으면 오류를 무시하고 다음 주소 검색

display.fill(0)                                 # 메모리의 모든 픽셀을 0으로 지움

display.text(I2CAddress, 0, 0, 1)               # 첫 줄: 검색한 I²C 주소를 좌상단에 표시
display.text("Shin Dong Woo", 0, 16, 1)         # 둘째 줄: 이름을 y=16 위치에 표시
display.text("Embedded System", 0, 32, 1)       # 셋째 줄: 문구를 y=32 위치에 표시

display.show()                                  # 버퍼에 작성한 내용을 실제 OLED 화면에 출력

bus.close()                                     # 사용한 I²C 버스를 닫고 자원을 해제