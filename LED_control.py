
import RPi.GPIO as GPIO
from time import sleep


#camera = PiCamera()
led = 23

#SETUP:
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

#ACTIVE FOR TWO SEC.
GPIO.output(led, GPIO.HIGH)

sleep(2)

GPIO.output(led, GPIO.LOW)

GPIO.cleanup()




