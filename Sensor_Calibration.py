import time
import RPi.GPIO as GPIO
from time import sleep
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import tifffile

# Set LED
led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

# Set camera controls
controls = {"ExposureTime": 5000000, #microseconds
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
time.sleep(1) # LED on for 2 seconds

#Capture image in unpacked RAW format 12bit dynamic range (16bit dataframe)
raw = picam2.capture_array("raw").view(np.uint16)

time.sleep(1)
GPIO.output(led, GPIO.LOW) # Turn off LED

#print(raw.shape)
#print(raw)
print(picam2.stream_configuration("raw"))
print(picam2.capture_metadata())
picam2.stop_preview()

# apply threshold to raw image
threshold = 100 # set threshold value
mask = np.where(raw > threshold, 1, 0)
raw_threshold = np.multiply(raw, mask)

# find first and last non-zero indices along each axis
y, x = np.nonzero(mask)
x_min, x_max = np.min(x), np.max(x)
y_min, y_max = np.min(y), np.max(y)

# create crop specification
crop_spec = (x_min, y_min, x_max-x_min, y_max-y_min)
print(crop_spec)

# crop the image
raw_cropped = raw[y_min:y_max, x_min:x_max]

# Min-Max Normalize 12-bit sensor data to fit 16-bit dataframe
#norm_image = np.zeros((3040,4064))
#norm_raw = cv2.normalize(raw,norm_image,0,65535,cv2.NORM_MINMAX,-1)
#print(norm_raw)

#raw_crop = norm_raw[0:3040, 0:4056] # Remove padding from each row of pixels

tifffile.imwrite('/home/martin/Desktop/raw_image.tiff', raw_threshold ) #Save RAW image

#Get color channels in bayer order (BGGR)
red =raw_cropped[1::2,1::2]
green1 = raw_cropped[0::2,1::2]
green2 = raw_cropped[1::2,0::2]
green = np.add(green1,green2)/2
blue = raw_croppped[0::2,0::2]

# save images with updating suffix (Red Channel)
suffix_red = 1
base_filename_red = "Red_channel"
save_dir_red = '/home/martin/Desktop/Images/Red/'
found = False

while not found:
    filename_red = f'{base_filename_red}{suffix_red}.tiff'
    if not os.path.exists(os.path.join(save_dir_red, filename_red)):
        found = True
    else:
        suffix_red += 1
        
tifffile.imwrite(os.path.join(save_dir_red, filename_red), red)
print("Red image saved")

# Save a stacked image of the red channel
stack_dir_red ='/home/martin/Desktop/Images/Red'
files_red = [f for f in os.listdir(stack_dir_red) if f.endswith('.tiff')]
files_red.sort()
#print(files_red)
stack_red = []

for file_red in files_red:
    stack_red.append(tifffile.imread(os.path.join(stack_dir_red, file_red)))
    
stacked_image_red = np.stack(stack_red, axis=0)

tifffile.imwrite('/home/martin/Desktop/Images/Red/Stack/stacked_red_channel.tiff', stacked_image_red)

#print(stack_red)
#print(stacked_image_red)
print(stacked_image_red.shape)


# save images with updating suffix (Green Channel)
suffix_green = 1
base_filename_green = "Green_channel"
save_dir_green = '/home/martin/Desktop/Images/Green/'
found = False

while not found:
    filename_green = f'{base_filename_green}{suffix_green}.tiff'
    if not os.path.exists(os.path.join(save_dir_green, filename_green)):
        found = True
    else:
        suffix_green += 1
        
tifffile.imwrite(os.path.join(save_dir_green, filename_green), green)
print("Green image saved")

# Save a stacked image of the GREEN channel
stack_dir_green ='/home/martin/Desktop/Images/Green'
files_green = [f for f in os.listdir(stack_dir_green) if f.endswith('.tiff')]
files_green.sort()
#print(files_green)
stack_green = []

for file_green in files_green:
    stack_green.append(tifffile.imread(os.path.join(stack_dir_green, file_green)))
    
stacked_image_green = np.stack(stack_green, axis=0)

tifffile.imwrite('/home/martin/Desktop/Images/Green/Stack/stacked_green_channel.tiff', stacked_image_green)
#print(stack_green)
#print(stacked_image_green.shape)

# Get the ratio of Red/Green pixel values in each plane of the stacked images
#with open('/home/martin/Desktop/ratios.txt', 'w') as f:
 #   f.write('Plane\tAverage Ratio\tAir Saturation\n')
  #  f.close()

stacked_image_red_avg = np.mean(stacked_image_red, axis=(1,2), dtype=float)
stacked_image_green_avg = np.mean(stacked_image_green, axis=(1,2), dtype=float)
#print(stacked_image_red_avg)

ratio = np.divide(stacked_image_red_avg, stacked_image_green_avg)

print("this is length of ratio", len(ratio), " and shape" , ratio.shape)
print(ratio)
plane_index = ratio.shape[0] - 1
print("max index", plane_index)
plane_ratio = ratio[plane_index]
print(" this ratio goes to file", plane_ratio)
plane_number = plane_index + 1
print(" this number goes to file", plane_number)

air_sat = 100

#plane_numbers = np.arange(1, ratio.shape[0] +1)

#air_sat = np.full(ratio.shape[0], 100)

data = np.column_stack((plane_number, plane_ratio, air_sat))
print(data)

if not os.path.exists('/home/martin/Desktop/ratios.txt'):
    with open ('/home/martin/Desktop/ratios.txt', 'w') as f:
        f.write('Plane\tAverage Ratio\tAir Saturation\n')

with open('/home/martin/Desktop/ratios.txt', 'a') as f:
    for row in data:
        f.write('{}\t{:.2f}\t{:.2f}\n'.format(int(row[0]), row[1], row[2]))
    f.flush()
    f.close()


GPIO.cleanup()
