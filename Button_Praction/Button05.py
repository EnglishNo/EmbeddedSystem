from gpiozero import Button, LED                # 입력·출력 클래스
from signal import pause                        # 메인 실행 흐름 대기

button = Button(17)                             # BCM 17번 버튼, 내부 풀업
led = LED(18)                                   # BCM 18번 LED 출력(초기 OFF)

button.when_pressed = led.on                    # 누르면 켜기
button.when_released = led.off                  # 떼면 끄기

# led.on과 led.off는 괄호 없이 메서드 자체를 등록
try:
    pause()                                     # 프로그램을 유지하며 이벤트 처리
# 종료 시 LED를 끄고 자원 정리
finally:
    led.off()                                   # LED 끄기

    button.close()                              # 입력 GPIO 자원 반환
    led.close()                                 # 출력 GPIO 자원 반환
