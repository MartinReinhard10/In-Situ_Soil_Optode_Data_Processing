import tkinter as tk
import tkinter as tkk


# EXIT GUI Command
def exit_app():
        thf.dhtDevice.exit()
        root.destroy()

# GUI Layout and function
root = tk.Tk()
root.title("Control For Optode Platform")
root.config()

main_frame = tk.Frame(root, width=1000, height=1000)
main_frame.grid(row=0, column=0,padx=20,pady=20)

exit_button = tk.Button(main_frame, text="Exit", fg="red", font=("Arial",20)).grid(row=10,column=10,padx=5,pady=5)

# Message window
text_widget_label = tk.Label(main_frame, text= "Status Box:", font="Arial").grid(row=0,column=3,padx=5,pady=5)
text_widget = tk.Text(main_frame, height=20, width=20)
text_widget.grid(row=1, column=3, padx=2, pady=5)

#Manual motor control Frame
motor_control=tk.Frame(main_frame,width=500,height=500)
motor_control.grid(row=1,column=1, padx=10, pady=10)
tk.Label(main_frame,text="Manual Motor Controls:", font="Arial").grid(row=0,column=1,padx=5,pady=5)

# Set Step Speed
def set_step_speed(speed):
    mf.set_step_speed(speed_scale.get())
speed_label = tk.Label(motor_control, text="Step Speed Control:").grid(row=0,column=0,padx=1,pady=1)
speed_scale = tk.Scale(motor_control, from_=0.0001, to=0.0005, resolution=0.0001, orient=tk.HORIZONTAL)
speed_scale.configure(length=200)
speed_scale.grid(row=0,column=1,padx=1,pady=1)
speed_scale.bind("<ButtonRelease-1>", set_step_speed)

# Create the vertical motor control frame
def set_steps_vertical(steps_v):
    mf.set_steps_vertical(vertical_steps_entry.get())
vertical_direction_button = tk.Button(motor_control, text="Down").grid(row=4,column=0,padx=1,pady=1)
vertical_direction_button = tk.Button(motor_control, text="Up").grid(row=4,column=1,padx=1,pady=1)
vertical_steps_label = tk.Label(motor_control, text="Vertical Steps: ").grid(row=2,column=0,padx=10,pady=10)
vertical_steps_entry = tk.Entry(motor_control)
vertical_steps_entry.grid(row=2,column=1,padx=1,pady=1)
vertical_steps_entry.bind("<KeyRelease>", set_steps_vertical)

# Create the rotate motor control frame
def set_steps_horizontal(steps_h):
    mf.set_steps_horizontal(horizontal_steps_entry.get())

horizontal_direction_button = tk.Button(motor_control, text="Left").grid(row=5,column=0,padx=1,pady=1)
horizontal_direction_button = tk.Button(motor_control, text="Right").grid(row=5,column=1,padx=1,pady=1)
horizontal_steps_label = tk.Label(motor_control, text="Horizontal Steps: ").grid(row=3,column=0,padx=10,pady=10)
horizontal_steps_entry = tk.Entry(motor_control)
horizontal_steps_entry.grid(row=3,column=1,padx=1,pady=1)
horizontal_steps_entry.bind("<KeyRelease>", set_steps_horizontal)

#Move "HOME" 
home_button = tk.Button(motor_control, text="Move to Bottom Position").grid(row=6,column=0,padx=10,pady=10)

# Distance Sensor
distance_label = tk.Label(motor_control, text="Distance from Bottom:")
distance_label.grid(row=7,column=0,padx=10,pady=10)


# Temperature and humidity 
temp_humid_frame = tk.Frame(main_frame,width=100,height=100)
temp_humid_frame.grid(row=5,column=3,padx=1,pady=1)
temp_label = tk.Label(temp_humid_frame, text="Temperature:")
temp_label.grid(row=1,column=1,padx=1,pady=1)
humidity_label = tk.Label(temp_humid_frame, text="Humidity:")
humidity_label.grid(row=1,column=3,padx=1,pady=1)


# Camera functions
camera_frame = tk.Frame(main_frame, width=200,height=500)
camera_frame.grid(row=1,column=2,padx=10,pady=10)
camera_frame_title = tk.Label(main_frame, text= "Camera Functions:",font="Arial").grid(row=0,column=2,padx=5,pady=5)

preview_button = tk.Button(camera_frame, text="Start Live Preview").grid(row=0,column=0,padx=5,pady=5)
stop_preview_button = tk.Button(camera_frame,text="Stop Live Preview").grid(row=0,column=1,padx=5,pady=5)
camera_jpeg_button = tk.Button(camera_frame, text="Capture Single JPEG Image").grid(row=1,column=0,padx=5,pady=5)
camera_raw_button = tk.Button(camera_frame, text="Capture Single RAW Image").grid(row=4,column=0,padx=1,pady=1)

exposure_label = tk.Label(camera_frame, text= "Exposure Time:").grid(row=2,column=0,padx=1,pady=1)
exposure_entry = tk.Entry(camera_frame)
exposure_entry.grid(row=2,column=1,padx=1,pady=1)

iso_label = tk.Label(camera_frame, text= "ISO:").grid(row=3,column=0,padx=1,pady=1)
iso_entry = tk.Entry(camera_frame)
iso_entry.grid(row=3,column=1,padx=1,pady=1)

#LED Control
def toggle_uv_state():
    global uv_state
    if uv_label.cget("text") == "ON":
        uv_label.config(text="OFF")
    else:
        uv_label.config(text="ON")
    
    uv_state = uv_label.cget("text") == "ON"

    message = f"state: {uv_state}\n"
    text_widget.insert('end', message)
    text_widget.see('end')
    
    
uv_label = tk.Label(camera_frame,text="OFF")
uv_label.grid(row=5,column=1,padx=5,pady=5)
uv_button =tk.Button(camera_frame,text="Toggle UV LED:", command=toggle_uv_state).grid(row=5,column=0,padx=5,pady=5)

#Show Histogram 
histogram_button = tk.Button(camera_frame, text= "RAW Channels Histogram").grid(row=4,column=1, padx=1,pady=1 )


o2_label = tk.Label(camera_frame, text="Enter O2 % Value:").grid(row=9,column=0,padx=1,pady=1)
o2_entry = tk.Entry(camera_frame)
o2_entry.grid(row=9,column=1,padx=1,pady=1)
delay_time_label = tk.Label(camera_frame, text="Set Delay Between Images:").grid(row=8,column=0,padx=1,pady=1)
delay_time_entry = tk.Entry(camera_frame)
delay_time_entry.grid(row=8,column=1,padx=1,pady=1)
num_images_label = tk.Label(camera_frame, text="Enter Number of Images:").grid(row=7,column=0, padx=1,pady=1 )
num_images_entry = tk.Entry(camera_frame)
num_images_entry.grid(row=7,column=1, padx=1,pady=1 )
capture_calibration_button = tk.Button(camera_frame, text="Capture Calibration Images").grid(row=10,column=0,padx=10,pady=10)
capture_calibration_label = tk.Label(camera_frame,text="Calibration Settings:", font=8).grid(row=6,column=0,padx=10,pady=10)

# Start GUI
root.mainloop()
