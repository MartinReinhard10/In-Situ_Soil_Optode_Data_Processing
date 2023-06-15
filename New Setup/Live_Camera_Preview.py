#Intialize Camera
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform

picam2 = Picamera2()

def start_preview():
   
    picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
    picam2.start()

def stop_preview():
    
    picam2.stop_preview()
    picam2.stop()
