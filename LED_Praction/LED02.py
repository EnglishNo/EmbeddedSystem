from gpiozero import LED  # gpiozero 라이브러리에서 LED 제어 클래스 불러오기
from time import sleep    # time 모듈에서 시간 대기(sleep) 함수 불러오기

# BCM 번호 기준 GPIO 17번 핀에 연결된 LED 객체 생성
led = LED(17)

try:
    led.on()       # LED 켜기 (GPIO 17번 핀에 HIGH/1 신호 출력)
    sleep(2)       # 2초 동안 대기
finally:
    # 예외 발생 여부와 상관없이 무조건 실행되어 안전한 종료 보장
    led.off()      # LED 끄기 (GPIO 17번 핀에 LOW/0 신호 출력)
    led.close()    # 사용이 끝난 GPIO 핀 자원 해제