import tkinter as tk
import time
import numpy as np
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform
import RPi.GPIO as GPIO
import board
import adafruit_dht
import busio
from adafruit_vl53l0x import VL53L0X
import Live_Camera_Preview as LCP


# GUI Layout and function
root = tk.Tk()
root.title("Control For Optode Platform")
root.config(bg="orange")

main_frame = tk.Frame(root, width=200, height=400)
main_frame.grid(row=1, column=0,padx=10,pady=5)

exit_button = tk.Button(root, text="Exit").grid(row=2,column=0,padx=1,pady=1)

#Preview Function#
preview_frame= tk.Frame(root,width=200,height=100)
preview_frame.grid(row=0,column=0,padx=5,pady=5)

# Button to start the camera preview
preview_button = tk.Button(preview_frame, text="Start Live Preview", command= LCP.start_preview)
preview_button.pack()

# Button to stop the camera preview
stop_preview_button = tk.Button(preview_frame,text="Stop Live Preview", command=LCP.stop_preview)
stop_preview_button.pack()

# Start GUI
root.mainloop()