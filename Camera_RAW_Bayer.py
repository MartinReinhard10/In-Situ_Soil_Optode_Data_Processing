import time
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
import cv2
import numpy as np
import matplotlib.pyplot as plt


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

# Set camera controls
controls = {"ExposureTime": 100000, #microseconds
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
 
time.sleep(5)

#Capture image in unpacked RAW format 12bit dynamic range (16bit dataframe)
raw = picam2.capture_array("raw").view(np.uint16) 
print(raw.shape)
print(raw)
print(picam2.stream_configuration("raw"))
print(picam2.capture_metadata())
picam2.stop_preview()

# Min-Max Normalize 12-bit sensor data to fit 16-bit dataframe
norm_image = np.zeros((3040,4064))
norm_raw = cv2.normalize(raw,norm_image,0,65535,cv2.NORM_MINMAX,-1)
print(norm_raw)

raw_crop = norm_raw[0:3040, 0:4056] # Remove padding from each row of pixels

cv2.imwrite('/home/martin/Desktop/raw_image.tiff', norm_raw) #Save RAW image

#Get color channels in bayer order (BGGR)
red =raw_crop[1::2,1::2]
green1 = raw_crop[0::2,1::2]
green2 = raw_crop[1::2,0::2]
green = np.add(green1,green2)/2
blue = raw_crop[0::2,0::2]

#Save images for each color in Bayer filter
cv2.imwrite('/home/martin/Desktop/red_bayer.tiff',red)
cv2.imwrite('/home/martin/Desktop/green_bayer.tiff',green1)
cv2.imwrite('/home/martin/Desktop/blue_bayer.tiff',blue)
print("Saved_images")




