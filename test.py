from smbus2 import SMBus

# I²C 버스 1번 사용
bus = SMBus(1)

# 연결된 장치의 주소 검색
for address in range(0x03, 0x78):
    try:
        bus.read_byte(address)
        print(f"I2C 장치 발견: 0x{address:02X}")
    except OSError:
        pass

# I²C 버스 종료
bus.close()
