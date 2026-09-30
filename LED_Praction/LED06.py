from gpiozero import LED  # gpiozero 라이브러리에서 LED 제어 클래스 불러오기
from time import sleep    # time 모듈에서 시간 대기(sleep) 함수 불러오기

# BCM 번호 기준 GPIO 17번 핀에 연결된 LED 객체 생성
led = LED(17)

# 정상(OK) 상태 표시 함수: 1초 간격으로 천천히 점멸 (켜짐 1.0초, 꺼짐 1.0초)
def show_ok():
    led.blink(1.0, 1.0)

# 경고(Warning) 상태 표시 함수: 0.2초 간격으로 빠르게 점멸 (켜짐 0.2초, 꺼짐 0.2초)
def show_warning():
    led.blink(0.2, 0.2)

# 에러(Error) 상태 표시 함수: 짧게 3번 반짝인 후 휴식 패턴 실행
def show_error():
    led.off()                    # LED 상태 초기화 (끄기)
    for _ in range(3):           # 3회 빠른 경고 점멸 반복
        led.on();  sleep(0.1)    # 0.1초 동안 켜기
        led.off(); sleep(0.1)    # 0.1초 동안 끄기
    sleep(1.5)                   # 패턴 완료 후 1.5초 동안 대기