import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN = 21
GPIO.setup(PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(PIN) == GPIO.HIGH:
        print("HIGH")
    else:
        print("LOW")
    time.sleep(0.1)