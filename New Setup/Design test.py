import tkinter as tk
from tkinter import ttk
import Live_Camera_Preview as LCP
import Motor_Function as mf
import Distance_sensor_Function as dsf
import Temp_Humid_Function as thf

def set_step_speed(speed):
    mf.set_step_speed(speed_scale.get())

def set_steps_vertical(steps_v):
    mf.set_steps_vertical(vertical_steps_entry.get())

def set_steps_horizontal(steps_h):
    mf.set_steps_horizontal(horizontal_steps_entry.get())

root = tk.Tk()
root.title("Control for Optode Platform")
root.config(bg="white")

# Main Frame
main_frame = ttk.Frame(root, width=200, height=400)
main_frame.grid(row=1, column=0, padx=10, pady=5)

# Exit Button
exit_button = ttk.Button(root, text="Exit")
exit_button.grid(row=2, column=0, padx=1, pady=1)

# Preview Frame
preview_frame = ttk.Frame(root, width=200, height=100)
preview_frame.grid(row=0, column=0, padx=5, pady=5)

# Button to start the camera preview
preview_button = ttk.Button(preview_frame, text="Start Live Preview", command=lcp.start_preview)
preview_button.pack()

# Button to stop the camera preview
stop_preview_button = ttk.Button(preview_frame, text="Stop Live Preview", command=lcp.stop_preview)
stop_preview_button.pack()

# Manual motor control Frame
motor_control = ttk.Frame(main_frame, width=100, height=185)
motor_control.grid(row=2, column=0, padx=5, pady=5)
ttk.Label(main_frame, text="Manual Motor Control", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5)

# Set Step Speed
speed_label = ttk.Label(motor_control, text="Step Speed Control:")
speed_label.grid(row=1, column=0, padx=1, pady=1)
speed_scale = ttk.Scale(motor_control, from_=0.0001, to=0.0005, resolution=0.0001, orient=tk.HORIZONTAL)
speed_scale.configure(length=200)
speed_scale.grid(row=1, column=1, padx=1, pady=1)
speed_scale.bind("<ButtonRelease-1>", set_step_speed)

# Create the vertical motor control frame
vertical_label = ttk.Label(motor_control, text="Move Vertical:")
vertical_label.grid(row=2, column=0, padx=0, pady=0)
vertical_direction_button = ttk.Button(motor_control, text="Down", command=lambda: mf.move_vertical_DOWN(mf.num_steps_vertical))
vertical_direction_button.grid(row=2, column=1, padx=1, pady=1)
vertical_direction_button = ttk.Button(motor_control, text="Up", command=lambda: mf.move_vertical_UP(mf.num_steps_vertical))
vertical_direction_button.grid(row=2, column=2, padx=1, pady=1)
vertical_steps_label = ttk.Label(motor_control, text="Steps: ")
vertical_steps_label.grid(row=2, column=3, padx=1, pady=1)
vertical_steps_entry = ttk.Entry(motor_control)
vertical_steps_entry.grid(row=2, column=4, padx=1, pady=1)
vertical_steps_entry.bind("<KeyRelease>", set_steps_vertical)

# Create the rotate motor control frame
horizontal_label = ttk.Label(motor_control, text="Move Horizontal:")
horizontal_label.grid(row=3, column=0, padx=0, pady=0)
horizontal_direction_button = ttk.Button(motor_control, text="Left", command=lambda:mf.rotate_LEFT(mf.num_steps_horizontal))
horizontal_direction_button.grid(row=3, column=1, padx=1, pady=1)
horizontal_direction_button = ttk.Button(motor_control, text="Right", command=lambda: mf.rotate_RIGHT(mf.num_steps_horizontal))
horizontal_direction_button.grid(row=3, column=2, padx=1, pady=1)
horizontal_steps_label = ttk.Label(motor_control, text="Steps: ")
horizontal_steps_label.grid(row=3, column=3, padx=1, pady=1)
horizontal_steps_entry = ttk.Entry(motor_control)
horizontal_steps_entry.grid(row=3, column=4, padx=1, pady=1)
horizontal_steps_entry.bind("<KeyRelease>", set_steps_horizontal)

# Distance Sensor
distance_label = ttk.Label(motor_control, text="Distance from Bottom: ")
distance_label.grid(row=4, column=0, padx=1, pady=1)
dsf.measure_distance(distance_label)

# Temperature and humidity 
temp_humid_frame = ttk.Frame(main_frame, width=100, height=100)
temp_humid_frame.grid(row=5, column=1, padx=1, pady=1)
temp_label = ttk.Label(temp_humid_frame, text="Temperature:")
temp_label.grid(row=1, column=1, padx=1, pady=1)
humidity_label = ttk.Label(temp_humid_frame, text="Humidity:")
humidity_label.grid(row=1, column=3, padx=1, pady=1)
thf.update_temp_values(temp_label, humidity_label)

# Start GUI
root.mainloop()
