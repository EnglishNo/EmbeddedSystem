from gpiozero import LED
from time import sleep

led = LED(17)
try:
    led.on()
    sleep(2)
finally:
    led.off()
    led.close()
