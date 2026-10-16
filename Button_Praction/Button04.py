from gpiozero import Button         # 버튼 입력 클래스
from signal import pause            # 메인 실행 흐름 대기

button = Button(17)                 # BCM 17번, 내부 풀업 사용

# 누름 시작: HIGH에서 LOW로 변화
def pressed():
    print("PRESSED")

# 해제: LOW에서 HIGH로 변화
def released():
    print("RELEASED")

button.when_pressed = pressed       # 눌림 콜백 등록
button.when_released = released     # 해제 콜백 등록

# 프로그램을 유지하며 이벤트 처리
try:
    pause()
# 종료 시 자원 정리
finally:
    button.close()                  # GPIO 자원 반환
