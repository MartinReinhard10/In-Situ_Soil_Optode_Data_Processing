from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform
import RPi.GPIO as GPIO
import cv2
import tifffile
import matplotlib.pyplot as plt
import time
import numpy as np

# Set LED Pin
led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

# Intialize Camera
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (4056, 3040)},
    lores={"size": (640, 480)},
    display="lores",
    transform=Transform(hflip=1, vflip=1),
)
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
    picam2.stop()
    plt.imshow(image)
    plt.show()
    print("Image Ready")

# Capture single RAW image
def capture_raw():
    # Set camera controls
    controls = {"ExposureTime": 3000000, #microseconds
            "AnalogueGain":1.0, # 1 = ISO 100
            "AeEnable": False, # Auto exposure and Gain
            "AwbEnable": False,# Auto white Balance
            "FrameDurationLimits": (114,239000000)} #Min/Max frame duration

    # Setup config parameters
    preview_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR12",},
                                                     controls = controls) 
    picam2.configure(preview_config)

    GPIO.output(led, GPIO.HIGH) # Turn on LED

    picam2.start() # Start Camera
 
    time.sleep(2)

    #Capture image in unpacked RAW format 12bit dynamic range (16bit array)
    raw = picam2.capture_array("raw").view(dtype="uint16")

    GPIO.output(led, GPIO.LOW) # Turn off LED

    #print(picam2.stream_configuration("raw"))
    print(picam2.capture_metadata())

    picam2.stop()

    plt.imshow(raw, cmap="gray")
    plt.show()
    print("RAW Ready")
    
 