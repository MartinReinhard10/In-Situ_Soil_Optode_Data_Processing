import board
import busio
import time
from adafruit_vl53l0x import VL53L0X

i2c = busio.I2C(board.SCL, board.SDA)

tof = VL53L0X(i2c)

while True:
    print("Distance: {} mm".format(tof.range))
    time.sleep(1.0)
