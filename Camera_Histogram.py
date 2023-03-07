import time
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
import cv2
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from time import sleep
import tifffile

# Set LED
led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

# Set camera controls
controls = {"ExposureTime": 4000000, #microseconds
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
 
time.sleep(2)

GPIO.output(led, GPIO.HIGH) # Turn on LED
time.sleep(1)

#Capture image in unpacked RAW format 12bit dynamic range (16bit array)
raw = picam2.capture_array("raw").view(np.uint16)

time.sleep(1)
GPIO.output(led, GPIO.LOW) # Turn off LED


print(picam2.stream_configuration("raw"))
print(picam2.capture_metadata())

picam2.stop_preview()


# Min-Max Normalize 12-bit sensor data to fit 16-bit dataframe
norm_image = np.zeros((3040,4064))
norm_raw = cv2.normalize(raw,norm_image,0,65535,cv2.NORM_MINMAX,-1)
#print(norm_raw)

raw_crop = norm_raw[0:3040, 0:4056] # Remove padding from each row of pixels
center_crop = raw[1000:2000, 2000:3000]

#tifffile.imwrite('/home/martin/Desktop/raw_image.tiff', center_crop) #Save RAW image

#Get color channels in bayer order (BGGR)
red = center_crop[1::2,1::2]
green1 = center_crop[0::2,1::2]
green2 = center_crop[1::2,0::2]
green = np.add(green1,green2)/2
blue = raw_crop[0::2,0::2]

#Make histogram for red and green channel # Set camera controls to have good pixel saturation
Colors=("red","green")
Channel_ids=(red,green)
for channel_id, c in zip(Channel_ids,Colors):
    histogram, bin_edges=np.histogram(channel_id,bins=4095, range=(0,4095))
    plt.plot(bin_edges[0:-1],histogram,color=c)
plt.title("Red_Green histogram")
plt.xlabel("Pixel intensity")
plt.ylabel("Pixel Frequency")
plt.show()
print("Histogram Succes")

# Count number of red and green pixels
num_red_pixels = np.count_nonzero(red)
num_green_pixels = np.count_nonzero(green)

print("Number of red pixels:", num_red_pixels)
print("Number of green pixels:", num_green_pixels)

GPIO.cleanup()