from gpiozero import Button             # 버튼 입력 클래스
from signal import pause                # 메인 실행 흐름 대기

# 내부 풀업을 사용하는 입력
button = Button(
    17,                 # BCM GPIO17 사용
    bounce_time=0.1,    # 디바운스 시간 0.1초
    hold_time=2.0       # 2초 유지하면 held 이벤트
)

# 누름 시작에 호출(길게 눌러도 실행)
def pressed():
    print("짧게 누름")  # 이 문구는 짧은 누름 판정이 아님

# 2초 유지 후 추가 호출(기본 1회)
def held():
    print("2초 이상 누름")

button.when_pressed = pressed           # 누름 시작 콜백
button.when_held = held                 # 길게 유지 콜백

try:
    pause()                             # 프로그램을 유지하며 이벤트 처리
finally:
    button.close()
