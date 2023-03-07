import RPi.GPIO as GPIO
import time

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

# Move motor one step
def step(step_pin):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(step_speed)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(step_speed)

# Move vertical motor a certain number of steps
def move_vertical(steps):
    GPIO.output(VERTICAL_DIR_PIN, VERTICAL_DIRECTION)
    for i in range(steps):
        step(VERTICAL_STEP_PIN)

# Rotate motor a certain number of steps
def rotate(steps):
    GPIO.output(ROTATE_ENABLE_PIN, GPIO.LOW)
    GPIO.output(ROTATE_DIR_PIN, ROTATE_DIRECTION)
    for i in range(steps):
        step(ROTATE_STEP_PIN)
    GPIO.output(ROTATE_ENABLE_PIN, GPIO.HIGH)

# Example usage
num_steps = 200
rotate_steps = 200
step_speed = 0.0005

move_vertical(num_steps) # Move vertical motor a certain number of steps
rotate(rotate_steps) # Rotate motor a certain number of steps
