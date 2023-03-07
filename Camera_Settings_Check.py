import time
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
import cv2
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from time import sleep
import tifffile
import os

# Set LED
led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

Exposure = 6000000
Led_Time = 2

# Set camera controls
controls = {"ExposureTime": Exposure, #microseconds
            "AnalogueGain":1.0, # 1 = ISO 100
            "AeEnable": False, # Auto exposure and Gain
            "AwbEnable": False,# Auto white Balance
            "FrameDurationLimits": (114,239000000)} #Min/Max frame duration

# Setup config parameters
preview_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR12",},
                                                     controls = controls) 
print(preview_config)
picam2.configure(preview_config)

picam2.start() # Start Camera

# Set the number of iterations
num_iterations = 1

# Open file for appending
filename = '/home/martin/Desktop/medians.txt'
file_exists = os.path.isfile(filename)

# Open file for appending REMEMBER to create file and change path accordingly!!
with open(filename, 'a') as f:
    if not file_exists:
        f.write('Iteration\tMedian Green\tMedian Red\tExposure\tLED Time\n')

    for i in range(num_iterations):
        time.sleep(3)

        GPIO.output(led, GPIO.HIGH) # Turn on LED

        time.sleep(Led_Time) # LED on for 2 seconds

        # Capture image in unpacked RAW format 12bit dynamic range (16bit array)
        raw = picam2.capture_array("raw").view(np.uint16)
        time.sleep(Led_Time)       
        GPIO.output(led, GPIO.LOW) # Turn off LED


        print(picam2.stream_configuration("raw"))
        print(picam2.capture_metadata())

        center_crop = raw[1000:2000, 2000:3000]


        #Get color channels in bayer order (BGGR)
        red = center_crop[1::2,1::2]
        green1 = center_crop[0::2,1::2]
        green2 = center_crop[1::2,0::2]
        green = np.add(green1,green2)/2

        # Calculate median pixel intensity of green and red channels
        median_green = np.median(green)
        median_red = np.median(red)

        # Write results to file
        f.write(f'{i+1}\t{median_green}\t{median_red}\t{Exposure}\t{Led_Time}\n')

        time.sleep(1)

picam2.stop_preview()

GPIO.cleanup()
