from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform
import matplotlib.pyplot as plt
import time

#Intialize Camera
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (4056,3040)}, lores={"size": (640,480)}, display="lores")
picam2.configure(camera_config)

# Preview 
def start_preview():
    picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
    picam2.start()

def stop_preview():
    picam2.stop_preview()
    picam2.stop()

# Capture single JPEG image

def capture_jpeg():
    picam2.start()
    time.sleep(3)
    image = picam2.capture_image()
    plt.imshow(image)

