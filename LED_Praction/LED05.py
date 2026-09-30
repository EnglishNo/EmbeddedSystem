from gpiozero import PWMLED  # gpiozero 라이브러리에서 PWM(밝기 조절) LED 제어 클래스 불러오기
from time import sleep      # time 모듈에서 시간 대기(sleep) 함수 불러오기

# BCM 번호 기준 GPIO 17번 핀에 연결된 PWM LED 객체 생성
led = PWMLED(17)

try:
    # 0.0(0%)부터 1.0(100%)까지 밝기를 25%씩 단계별로 순회
    for value in [0.0, 0.25, 0.5, 0.75, 1.0]:
        led.value = value              # LED 밝기 설정 (0.0: 완전 꺼짐 ~ 1.0: 최대 밝기)
        print(f"duty={value:.2f}")     # 현재 설정된 밝기(Duty Cycle) 값 출력
        sleep(2)                       # 해당 밝기를 2초 동안 유지

    # 1초 동안 밝아지고 1초 동안 어두워지는 페이드(pulse) 효과 실행
    led.pulse(fade_in_time=1, fade_out_time=1)
    sleep(6)                           # pulse 효과가 6초 동안 작동하도록 대기 (총 3회 반복)
finally:
    # 예외 발생 여부와 상관없이 무조건 실행되어 안전한 종료 보장
    led.close()                        # 사용이 끝난 GPIO 핀 자원 해제