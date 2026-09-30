from gpiozero import LED  # gpiozero 라이브러리에서 LED 제어 클래스 불러오기
from signal import pause  # signal 모듈에서 프로세스 대기(pause) 함수 불러오기

# BCM 번호 기준 GPIO 17번 핀에 연결된 LED 객체 생성
led = LED(17)

# 0.2초 동안 켜지고 0.8초 동안 꺼지는 패턴을 백그라운드(비동기)에서 무한 반복
led.blink(
    on_time=0.2,
    off_time=0.8
)

try:
    print("LED 깜빡이는 중... (종료하려면 Ctrl+C를 누르세요)")
    pause()        # 프로세스가 종료되지 않도록 무한 대기 (백그라운드 깜빡임 유지)
finally:
    # 키보드 인터럽트(Ctrl+C) 등 예외 발생 시 안전하게 실행
    led.close()    # 사용이 끝난 GPIO 핀 자원 해제