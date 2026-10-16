from gpiozero import Button     # 버튼 입력 클래스
from signal import pause        # 메인 실행 흐름 대기

button = Button(17)             # BCM 17번, 내부 풀업 사용

def pressed():                  # 눌림 이벤트에서 실행할 함수
    print("버튼을 눌렀습니다.")

# 함수 자체를 등록: pressed()처럼 호출하지 않음
button.when_pressed = pressed
try:
    pause()                     # 프로그램을 유지하며 이벤트 처리
finally:                        # Ctrl+C 등으로 종료할 때 정리
    button.close()              # GPIO 자원 반환
