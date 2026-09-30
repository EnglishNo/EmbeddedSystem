from gpiozero import LED
from time import sleep

led = LED(17)        # BCM GPIO17
led.on()
sleep(2)
led.off()
led.close()