from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import time
from libcamera import Transform

led = 23 #GPIO 23
#SETUP:
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (4056,3040)}, lores={"size": (640,480)}, display="lores", transform=Transform(hflip=1, vflip=1))
picam2.configure(camera_config)

#ACTIVE FOR TWO SEC.
picam2.start_preview(Preview.QTGL)

picam2.start()

GPIO.output(led, GPIO.HIGH)

time.sleep(2)

picam2.capture_file('/home/martin/Desktop/test.jpg')

GPIO.output(led, GPIO.LOW)

GPIO.cleanup()




















