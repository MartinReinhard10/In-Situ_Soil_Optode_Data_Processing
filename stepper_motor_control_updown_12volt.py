import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pin numbers for each motor
VERTICAL_STEP_PIN = 27
VERTICAL_DIR_PIN = 17
TOP_ENDSTOP_PIN = 23
BOTTOM_ENDSTOP_PIN = 24
ROTATE_STEP_PIN = 9
ROTATE_DIR_PIN = 10

# Set up pins as outputs
GPIO.setup(VERTICAL_STEP_PIN, GPIO.OUT)
GPIO.setup(VERTICAL_DIR_PIN, GPIO.OUT)
GPIO.setup(ROTATE_STEP_PIN, GPIO.OUT)
GPIO.setup(ROTATE_DIR_PIN, GPIO.OUT)

# Set up endstops as inputs
GPIO.setup(TOP_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOTTOM_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set motor direction 
DOWN = GPIO.HIGH
UP = GPIO.LOW

CW = GPIO.HIGH
CCW = GPIO.LOW

VERTICAL_DIRECTION = DOWN 
ROTATE_DIRECTION = CCW 

# Move motor one step
def step(step_pin):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(step_speed)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(step_speed)

# Move vertical motor a certain number of steps or until an endstop is triggered
def move_vertical(steps):
    GPIO.output(VERTICAL_DIR_PIN, VERTICAL_DIRECTION)
    for i in range(steps):
        if VERTICAL_DIRECTION == DOWN and GPIO.input(TOP_ENDSTOP_PIN) == GPIO.LOW:
            print("Top endstop reached")
            break
        elif VERTICAL_DIRECTION == UP and GPIO.input(BOTTOM_ENDSTOP_PIN) == GPIO.LOW:
            print("Bottom endstop reached")
            break
        step(VERTICAL_STEP_PIN)

# Rotate motor a certain number of steps
def rotate(steps):
    GPIO.output(ROTATE_DIR_PIN, ROTATE_DIRECTION)
    for i in range(steps):
        step(ROTATE_STEP_PIN)

# Example usage
num_steps = 200
rotate_steps = 200
step_speed = 0.0005

# Move vertical motor a certain number of steps or until an endstop is triggered
move_vertical(num_steps)

# Rotate motor a certain number of steps
rotate(rotate_steps)
