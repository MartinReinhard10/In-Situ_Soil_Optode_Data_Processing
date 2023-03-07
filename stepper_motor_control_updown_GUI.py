import RPi.GPIO as GPIO
import time
import tkinter as tk
from picamera2 import Picamera2, Preview
from libcamera import Transform

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
picam2.start()

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
VERTICAL_DIRECTION = DOWN
ROTATE_DIRECTION = ACW
current_direction = {'vertical': VERTICAL_DIRECTION, 'rotate': ROTATE_DIRECTION}

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
def set_step_speed():
    global step_speed
    step_speed = float(step_speed_entry.get())

# Create the main window
window = tk.Tk()
window.title("Motor Control")

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
step_speed_frame = tk.Frame(window)
step_speed_frame.pack()
step_speed_label = tk.Label(step_speed_frame, text="Step Speed Control")
step_speed_label.pack()
step_speed_entry = tk.Entry(step_speed_frame)
step_speed_entry.pack()
step_speed_button = tk.Button(step_speed_frame, text="Set Step Speed", command=set_step_speed)
step_speed_button.pack()

#Create the control buttons frame
control_frame = tk.Frame(window)
control_frame.pack()
move_vertical_button = tk.Button(control_frame, text="Move Vertical Motor", command=lambda: move_vertical(num_steps))
move_vertical_button.pack(side=tk.LEFT)
rotate_button = tk.Button(control_frame, text="Rotate Motor", command=lambda: rotate(num_steps))
rotate_button.pack(side=tk.LEFT)

#Run the main loop
window.mainloop()
