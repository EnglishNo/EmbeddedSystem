from gpiozero import Button     # 버튼 입력 클래스
from time import sleep          # 반복 사이의 대기 함수

button = Button(17)             # BCM 17번, 내부 풀업 사용

try:                            # 실행 후에는 finally에서 자원 정리
    while True:                 # 버튼 상태를 계속 확인
        if button.is_pressed:   # 누르면 True(전압은 LOW)
            print("PRESSED")    # 누르는 동안 반복 출력
        else:                   # 버튼을 떼고 있는 상태
            print("RELEASED")
        sleep(0.1)              # 0.1초 대기 후 다시 확인

finally:                        # Ctrl+C 등으로 벗어나도 정리
    button.close()              # GPIO 자원 반환