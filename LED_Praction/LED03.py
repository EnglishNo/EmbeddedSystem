from gpiozero import LED  # gpiozero 라이브러리에서 LED 제어 클래스 불러오기
from time import sleep    # time 모듈에서 시간 대기(sleep) 함수 불러오기

# BCM 번호 기준 GPIO 17번 핀에 연결된 LED 객체 생성
led = LED(17)

try:
    # 5회 반복 실행 (count: 0부터 4까지)
    for count in range(5):
        led.on()          # LED 켜기 (GPIO 17번 핀에 HIGH/1 신호 출력)
        sleep(0.8)        # 0.8초 동안 대기 (켜짐 유지)
        led.off()         # LED 끄기 (GPIO 17번 핀에 LOW/0 신호 출력)
        sleep(0.2)        # 0.2초 동안 대기 (꺼짐 유지)
        print(count + 1)  # 현재 깜빡인 횟수(1부터 5까지) 출력
finally:
    # 예외 발생 여부와 상관없이 무조건 실행되어 안전한 종료 보장
    led.close()           # 사용이 끝난 GPIO 핀 자원 해제