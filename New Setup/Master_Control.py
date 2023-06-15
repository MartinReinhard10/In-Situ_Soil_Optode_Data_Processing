from tkinter import tk
import numpy as np
import RPi.GPIO as GPIO
import board
import adafruit_dht
import busio
from adafruit_vl53l0x import VL53L0X
import Live_Camera_Preview as lcp
import Motor_Function as mf



#Intialize Camera
picam2 = Picamera2()

#Intialize Temperature Sensor
dhtDevice = adafruit_dht.DHT22(board.D8)

# EXIT GUI Command
def exit_app():
        dhtDevice.exit()
        window.destroy()

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
preview_button = tk.Button(preview_frame, text="Start Live Preview", command= lcp.start_preview)
preview_button.pack()

# Button to stop the camera preview
stop_preview_button = tk.Button(preview_frame,text="Stop Live Preview", command=lcp.stop_preview)
stop_preview_button.pack()

#Manual motor control Frame
motor_control=tk.Frame(main_frame,width=100,height=185)
motor_control.grid(row=2,column=0, padx=5, pady=5)
tk.Label(main_frame,text="Manual Motor Control").grid(row=1,column=0,padx=5,pady=5)

# Set Step Speed
speed_label = tk.Label(motor_control, text="Step Speed Control:").grid(row=1,column=0,padx=1,pady=1)
speed_scale = tk.Scale(motor_control, from_=0.0001, to=0.0005, resolution=0.0001, orient=tk.HORIZONTAL)
speed_scale.configure(length=200)
speed_scale.grid(row=1,column=1,padx=1,pady=1)
speed_scale.bind("<ButtonRelease-1>", mf.set_step_speed)

# Create the vertical motor control frame
vertical_label = tk.Label(motor_control, text="Move Vertical:").grid(row=2,column=0,padx=0,pady=0)
vertical_direction_button = tk.Button(motor_control, text="Down", command=mf.move_vertical_DOWN(mf.num_steps_vertical)).grid(row=2,column=1,padx=1,pady=1)
vertical_direction_button = tk.Button(motor_control, text="Up", command=mf.move_vertical_UP(mf.num_steps_vertical)).grid(row=2,column=2,padx=1,pady=1)
vertical_steps_label = tk.Label(motor_control, text="Steps: ").grid(row=2,column=3,padx=1,pady=1)
vertical_steps_entry = tk.Entry(motor_control)
vertical_steps_entry.grid(row=2,column=4,padx=1,pady=1)
vertical_steps_entry.bind("<KeyRelease>", mf.set_steps)

# Create the rotate motor control frame
horizontal_label = tk.Label(motor_control, text="Move Horizontal:").grid(row=3,column=0,padx=0,pady=0)
horizontal_direction_button = tk.Button(motor_control, text="Left", command=mf.rotate_LEFT(mf.num_steps_horizontal)).grid(row=3,column=1,padx=1,pady=1)
horizontal_direction_button = tk.Button(motor_control, text="Right", command=mf.rotate_RIGHT(mf.num_steps_horizontal)).grid(row=3,column=2,padx=1,pady=1)
horizontal_steps_label = tk.Label(motor_control, text="Steps: ").grid(row=3,column=3,padx=1,pady=1)
horizontal_steps_entry = tk.Entry(motor_control)
horizontal_steps_entry.grid(row=3,column=4,padx=1,pady=1)
horizontal_steps_entry.bind("<KeyRelease>", mf.set_steps)

# Distance Sensor
distance_label = tk.Label(motor_control, text="Distance from Bottom: ")
distance_label.grid(row=4,column=0,padx=1,pady=1)

# Temperature and humidity 
temp_humid_frame = tk.Frame(main_frame,width=100,height=100)
temp_humid_frame.grid(row=5,column=1,padx=1,pady=1)

temp_label = tk.Label(temp_humid_frame, text="Temperature:").grid(row=1,column=1,padx=1,pady=1)
temp_value = tk.Label(temp_humid_frame, text="-").grid(row=1,column=2,padx=1,pady=1)
humidity_label = tk.Label(temp_humid_frame, text="Humidity:").grid(row=1,column=3,padx=1,pady=1)
humidity_value = tk.Label(temp_humid_frame, text="-").grid(row=1,column=4,padx=1,pady=1)
start_button = tk.Button(temp_humid_frame, text="Start Temperature/humidity sensor (internal)").grid(row=1,column=0,padx=1,pady=1)

# Start GUI
root.mainloop()





















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
