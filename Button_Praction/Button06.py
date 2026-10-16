from gpiozero import Button, LED            # 입력·출력 클래스
from signal import pause                    # 메인 실행 흐름 대기

# BCM 17번, 내부 풀업, 디바운스 시간 0.1초
button = Button(17, bounce_time=0.1)
led = LED(18)                               # BCM 18번 LED 출력(초기 OFF)

# 눌릴 때마다 호출할 함수
def toggle_led():
    led.toggle()                            # 켜짐과 꺼짐을 서로 바꿈
    state = "ON" if led.is_lit else "OFF"   # 현재 상태
    print(f"LED={state}")                   # 변경된 상태 출력

button.when_pressed = toggle_led            # 눌림 콜백 등록

try:
    pause()                                 # 프로그램을 유지하며 이벤트 처리
# 종료 시 자원 정리
finally:
    led.off()  # LED 끄기
    button.close()  # 입력 GPIO 자원 반환
    led.close()  # 출력 GPIO 자원 반환
