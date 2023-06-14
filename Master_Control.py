import tkinter as tk
<<<<<<< HEAD

root = tk.Tk()

root.title("In Situ Sensor Control")
label = tk.Label(root, text="Hi")
label.pack()
root.mainloop()


=======
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

#good

picam2 = Picamera2()

dhtDevice = adafruit_dht.DHT22(board.D8)

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pin numbers for each motor
VERTICAL_STEP_PIN = 27
VERTICAL_DIR_PIN = 17
ROTATE_STEP_PIN = 9
ROTATE_DIR_PIN = 10
ROTATE_ENABLE_PIN = 11

# Set up pins as outputs
GPIO.setup(VERTICAL_STEP_PIN, GPIO.OUT)
GPIO.setup(VERTICAL_DIR_PIN, GPIO.OUT)
GPIO.setup(ROTATE_STEP_PIN, GPIO.OUT)
GPIO.setup(ROTATE_DIR_PIN, GPIO.OUT)
GPIO.setup(ROTATE_ENABLE_PIN, GPIO.OUT)

# Disable rotate motor by default
GPIO.output(ROTATE_ENABLE_PIN, GPIO.LOW)

# Set motor direction
DOWN = GPIO.HIGH
UP = GPIO.LOW
CW = GPIO.HIGH
ACW = GPIO.LOW
VERTICAL_DIRECTION = UP
ROTATE_DIRECTION = ACW
current_direction = {'vertical': VERTICAL_DIRECTION, 'rotate': ROTATE_DIRECTION}

def start_preview():
    picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
    picam2.start()

def stop_preview():
    picam2.stop_preview()
    picam2.stop()

# Move motor one step
def step(step_pin):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(step_speed)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(step_speed)

# Move vertical motor a certain number of steps
def move_vertical(steps):
    GPIO.output(VERTICAL_DIR_PIN, current_direction['vertical'])
    for i in range(steps):
        step(VERTICAL_STEP_PIN)

# Rotate motor a certain number of steps
def rotate(steps):
    GPIO.output(ROTATE_ENABLE_PIN, GPIO.LOW)
    GPIO.output(ROTATE_DIR_PIN, current_direction['rotate'])
    for i in range(steps):
        step(ROTATE_STEP_PIN)
    GPIO.output(ROTATE_ENABLE_PIN, GPIO.HIGH)

# Change vertical motor direction
def change_vertical_direction():
    global VERTICAL_DIRECTION
    VERTICAL_DIRECTION = not VERTICAL_DIRECTION
    current_direction['vertical'] = VERTICAL_DIRECTION
    vertical_direction_label_var.set('Down' if VERTICAL_DIRECTION else 'Up')

# Change rotate motor direction
def change_rotate_direction():
    global ROTATE_DIRECTION
    ROTATE_DIRECTION = not ROTATE_DIRECTION
    current_direction['rotate'] = ROTATE_DIRECTION
    rotate_direction_label_var.set('CW' if ROTATE_DIRECTION else 'ACW')

# Set the number of steps
def set_steps():
    global num_steps
    num_steps = int(steps_entry.get())

# Set the step speed
def set_step_speed(event):
    global step_speed
    step_speed = speed.get()

def start_measurement():
    global is_measuring
    is_measuring = True
    update_values()
        
def update_values():
    if is_measuring:
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            temp_value.config(text="{:.1f} F / {:.1f} C".format(temperature_f, temperature_c))
            humidity_value.config(text="{}%".format(humidity))
        except RuntimeError as error:
            temp_value.config(text="-")
            humidity_value.config(text="-")
            print(error.args[0])
    else:
        temp_value.config(text="-")
        humidity_value.config(text="-")
    
        # Update every 2 seconds
    window.after(2000, update_values)

def exit_app():
        dhtDevice.exit()
        window.destroy()

def update_distance(label):
    i2c = busio.I2C(board.SCL, board.SDA)
    tof = VL53L0X(i2c)
    distance_mm = tof.range
    label.config(text="Distance: {} mm".format(distance_mm))
    label.after(1000, update_distance, label)  # Update every second

# Create the main window
window = tk.Tk()
window.title("Optode Platform Control")
window.geometry("500x700")

# Add widgets and functionality here
 # Button to start the camera preview
preview_button = tk.Button(text="Start Live Preview", command=start_preview)
preview_button.pack(side="top")

# Button to stop the camera preview
stop_preview_button = tk.Button(text="Stop Live Preview", command=stop_preview)
stop_preview_button.pack(side="top")

# Create the vertical motor control frame
vertical_frame = tk.Frame(window)
vertical_frame.pack()
vertical_label = tk.Label(vertical_frame, text="Vertical Motor Control")
vertical_label.pack()
vertical_direction_button = tk.Button(vertical_frame, text="Change Direction", command=change_vertical_direction)
vertical_direction_button.pack()
vertical_direction_label = tk.Label(vertical_frame, text="Direction: ")
vertical_direction_label.pack()
vertical_direction_label_var = tk.StringVar()
vertical_direction_label_var.set('Down' if VERTICAL_DIRECTION else 'Up')
vertical_direction_value_label = tk.Label(vertical_frame, textvariable=vertical_direction_label_var)
vertical_direction_value_label.pack()
steps_label = tk.Label(vertical_frame, text="Steps: ")
steps_label.pack()
steps_entry = tk.Entry(vertical_frame)
steps_entry.pack()
steps_button = tk.Button(vertical_frame, text="Set Steps", command=set_steps)
steps_button.pack()

#Create the rotate motor control frame
rotate_frame = tk.Frame(window)
rotate_frame.pack()
rotate_label = tk.Label(rotate_frame, text="Rotate Motor Control")
rotate_label.pack()
rotate_direction_button = tk.Button(rotate_frame, text="Change Direction", command=change_rotate_direction)
rotate_direction_button.pack()
rotate_direction_label = tk.Label(rotate_frame, text="Direction: ")
rotate_direction_label.pack()
rotate_direction_label_var = tk.StringVar()
rotate_direction_label_var.set('CW' if ROTATE_DIRECTION else 'ACW')
rotate_direction_value_label = tk.Label(rotate_frame, textvariable=rotate_direction_label_var)
rotate_direction_value_label.pack()
steps_label = tk.Label(rotate_frame, text="Steps: ")
steps_label.pack()
steps_entry = tk.Entry(rotate_frame)
steps_entry.pack()
steps_button = tk.Button(rotate_frame, text="Set Steps", command=set_steps)
steps_button.pack()

#Create the step speed control frame
speed_frame = tk.Frame(window)
speed_frame.pack()

speed_label = tk.Label(speed_frame, text="Step Speed Control")
speed_label.pack()

speed = tk.Scale(speed_frame, from_=0.0001, to=0.0005, resolution=0.0001, orient=tk.HORIZONTAL)
speed.configure(length=200)
speed.pack()

speed.bind("<ButtonRelease-1>", set_step_speed)


#Create the control buttons frame
control_frame = tk.Frame(window)
control_frame.pack()
move_vertical_button = tk.Button(control_frame, text="Move Vertical Motor", command=lambda: move_vertical(num_steps))
move_vertical_button.pack(side=tk.LEFT)
rotate_button = tk.Button(control_frame, text="Rotate Motor", command=lambda: rotate(num_steps))
rotate_button.pack(side=tk.LEFT)

# Create widgets
# Create widgets
temp_humid_frame = tk.Frame(window)
temp_humid_frame.pack()

temp_label = tk.Label(temp_humid_frame, text="Temperature:")
temp_value = tk.Label(temp_humid_frame, text="-")
humidity_label = tk.Label(temp_humid_frame, text="Humidity:")
humidity_value = tk.Label(temp_humid_frame, text="-")
start_button = tk.Button(temp_humid_frame, text="Start Temp_Humod", command=start_measurement)
exit_button = tk.Button(temp_humid_frame, text="Exit", command=exit_app)
start_button.pack(side=tk.LEFT)
exit_button.pack(side=tk.BOTTOM)
temp_label.pack(side=tk.LEFT)
temp_value.pack(side=tk.LEFT)
humidity_label.pack(side=tk.LEFT)
humidity_value.pack(side=tk.LEFT)

distance_frame =tk.Frame(window)
distance_frame.pack()
distance_label = tk.Label(distance_frame, text="Distance: ")
distance_label.pack(side=tk.LEFT)
update_distance(distance_label)


# Start the GUI event loop
window.mainloop()
>>>>>>> bedbbc7273327a44667fd7054f13a9e90ba04716
