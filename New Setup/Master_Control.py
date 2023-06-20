import tkinter as tk
import Camera_Function as cf
import Motor_Function as mf
import Distance_sensor_Function as dsf
import Temp_Humid_Function as thf

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
def display_message(message):
    text_widget.insert('end', message + '\n')
    text_widget.see('end')  # Auto-scroll to the end

text_widget_label = tk.Label(main_frame, text= "Status Box:", font="Arial").grid(row=0,column=3,padx=5,pady=5)
text_widget = tk.Text(main_frame, height=20, width=20)
text_widget.grid(row=1, column=3, padx=2, pady=5)

#Preview Function#
preview_frame= tk.Frame(root,width=200,height=100)
preview_frame.grid(row=0,column=0,padx=5,pady=5)

# Button to start the camera preview
preview_button = tk.Button(preview_frame, text="Start Live Preview", command= cf.start_preview)
preview_button.pack()

# Button to stop the camera preview
stop_preview_button = tk.Button(preview_frame,text="Stop Live Preview", command=cf.stop_preview)
stop_preview_button.pack()

#Manual motor control Frame
motor_control=tk.Frame(main_frame,width=100,height=185)
motor_control.grid(row=2,column=0, padx=5, pady=5)
tk.Label(main_frame,text="Manual Motor Control").grid(row=1,column=0,padx=5,pady=5)

# Set Step Speed
def set_step_speed(speed):
    mf.set_step_speed(speed_scale.get())
speed_label = tk.Label(motor_control, text="Step Speed Control:").grid(row=1,column=0,padx=1,pady=1)
speed_scale = tk.Scale(motor_control, from_=0.0001, to=0.0005, resolution=0.0001, orient=tk.HORIZONTAL)
speed_scale.configure(length=200)
speed_scale.grid(row=1,column=1,padx=1,pady=1)
speed_scale.bind("<ButtonRelease-1>", set_step_speed)

# Create the vertical motor control frame
def set_steps_vertical(steps_v):
    mf.set_steps_vertical(vertical_steps_entry.get())
vertical_label = tk.Label(motor_control, text="Move Vertical:").grid(row=2,column=0,padx=0,pady=0)
vertical_direction_button = tk.Button(motor_control, text="Down", command=lambda: mf.move_vertical_DOWN(mf.num_steps_vertical)).grid(row=2,column=1,padx=1,pady=1)
vertical_direction_button = tk.Button(motor_control, text="Up", command=lambda: mf.move_vertical_UP(mf.num_steps_vertical)).grid(row=2,column=2,padx=1,pady=1)
vertical_steps_label = tk.Label(motor_control, text="Steps: ").grid(row=2,column=3,padx=1,pady=1)
vertical_steps_entry = tk.Entry(motor_control)
vertical_steps_entry.grid(row=2,column=4,padx=1,pady=1)
vertical_steps_entry.bind("<KeyRelease>", set_steps_vertical)

# Create the rotate motor control frame
def set_steps_horizontal(steps_h):
    mf.set_steps_horizontal(horizontal_steps_entry.get())
horizontal_label = tk.Label(motor_control, text="Move Horizontal:").grid(row=3,column=0,padx=0,pady=0)
horizontal_direction_button = tk.Button(motor_control, text="Left", command=lambda:mf.rotate_LEFT(mf.num_steps_horizontal)).grid(row=3,column=1,padx=1,pady=1)
horizontal_direction_button = tk.Button(motor_control, text="Right", command=lambda: mf.rotate_RIGHT(mf.num_steps_horizontal)).grid(row=3,column=2,padx=1,pady=1)
horizontal_steps_label = tk.Label(motor_control, text="Steps: ").grid(row=3,column=3,padx=1,pady=1)
horizontal_steps_entry = tk.Entry(motor_control)
horizontal_steps_entry.grid(row=3,column=4,padx=1,pady=1)
horizontal_steps_entry.bind("<KeyRelease>", set_steps_horizontal)

#Move "HOME" 
home_button = tk.Button(motor_control, text="Move to Bottom Position").grid(row=6,column=0,padx=10,pady=10)

#Move to set Distance
def set_distance(distance_trigger):
    global new_distance_value
    global current_distance_value
    new_distance_value = move_distance_entry.get()
    current_distance_value = dsf.median_distance

move_distance_button = tk.Button(motor_control, text="Move to Distance", command=lambda: mf.move_distance(new_distance_value,current_distance_value)).grid(row=7,column=0,padx=10,pady=10)
move_distance_entry = tk.Entry(motor_control)
move_distance_entry.grid(row=7,column=1,padx=10,pady=10)
move_distance_entry.bind("<KeyRelease>", set_distance)

# Distance Sensor
distance_label = tk.Label(motor_control, text="Distance from Bottom: ")
distance_label.grid(row=8,column=0,padx=1,pady=1)
dsf.measure_distance(distance_label)

# Temperature and humidity 
temp_humid_frame = tk.Frame(main_frame,width=100,height=100)
temp_humid_frame.grid(row=5,column=1,padx=1,pady=1)
temp_label = tk.Label(temp_humid_frame, text="Temperature:")
temp_label.grid(row=1,column=1,padx=1,pady=1)
humidity_label = tk.Label(temp_humid_frame, text="Humidity:")
humidity_label.grid(row=1,column=3,padx=1,pady=1)
thf.update_temp_values(temp_label, humidity_label)

# Camera functions
camera_frame = tk.Frame(main_frame, width=200,height=500)
camera_frame.grid(row=1,column=2,padx=5,pady=5)
camera_frame_title = tk.Label(main_frame, text= "Camera Functions:",font="Arial").grid(row=0,column=2,padx=5,pady=5)
camera_jpeg_button = tk.Button(camera_frame, text="Capture JPEG Image", command= cf.capture_jpeg).grid(row=0,column=0,padx=1,pady=1)
camera_raw_button = tk.Button(camera_frame, text="Capture RAW Image", command=lambda: cf.capture_raw(uv_state, exposure_time, iso_value)).grid(row=1,column=0,padx=1,pady=1)

# Camera Settings: Exposure and ISO
def set_exposure(exposure):
     global exposure_time
     exposure_time_get = exposure_entry.get() 
     exposure_time = int(float(exposure_time_get) * 10E5)
     display_message(f"exposure: {exposure_time}\n")
     

exposure_label = tk.Label(camera_frame, text= "Exposure Time (seconds):").grid(row=4,column=0,padx=1,pady=1)     
exposure_entry = tk.Entry(camera_frame)
exposure_entry.grid(row=4,column=1,padx=1,pady=1)
exposure_entry.bind("<KeyRelease>", set_exposure)

def set_iso(iso):
     global iso_value
     iso_value_get = iso_entry.get()
     iso_value = int(iso_value_get)
     display_message(f"ISO: {iso_value}\n")

iso_label = tk.Label(camera_frame, text= "ISO:").grid(row=5,column=0,padx=1,pady=1)
iso_entry = tk.Entry(camera_frame)
iso_entry.grid(row=5,column=1,padx=1,pady=1)
iso_entry.bind("<KeyRelease>", set_iso)

#LED Control
def toggle_uv_state():
    global uv_state
    if uv_label.cget("text") == "ON":
        uv_label.config(text="OFF")
    else:
        uv_label.config(text="ON")
    
    uv_state = uv_label.cget("text") == "ON"

    display_message(f"UV state: {uv_state}\n")
    
uv_label = tk.Label(camera_frame,text="OFF")
uv_label.grid(row=1,column=2,padx=1,pady=1)
uv_button =tk.Button(camera_frame,text="Toggle UV LED:", command=toggle_uv_state).grid(row=1,column=1,padx=1,pady=1)

#Show Histogram 
histogram_button = tk.Button(camera_frame, text= "Show Histogram", command=cf.display_histogram).grid(row=2,column=0, padx=1,pady=1 )

#Capture Calibration images 

def set_o2(o2_trigger):
    global o2_value
    o2_value = o2_entry.get()
    display_message(f"O2 %: {o2_value}\n")
    
def set_image_number(image_number_trigger):
    global num_images
    num_images = int(num_images_entry.get())
    display_message(f"number of images: {num_images}\n")

def set_delay(delay_trigger):
    global delay_time
    delay_time = int(delay_time_entry.get())
    display_message(f"Delay time: {delay_time}\n")

def capture_calibration_images():
    cf.capture_calibration(o2_value, num_images, exposure_time, iso_value, uv_state, delay_time)
    display_message("Calibration images captured.\n")

o2_label = tk.Label(camera_frame, text="Enter O2 % Value:").grid(row=7,column=0,padx=1,pady=1)
o2_entry = tk.Entry(camera_frame)
o2_entry.grid(row=7,column=1,padx=1,pady=1)
o2_entry.bind("<KeyRelease>", set_o2)
delay_time_label = tk.Label(camera_frame, text="Set Delay Between Images:").grid(row=8,column=0,padx=1,pady=1)
delay_time_entry = tk.Entry(camera_frame)
delay_time_entry.grid(row=8,column=1,padx=1,pady=1)
delay_time_entry.bind("<KeyRelease>", set_delay)
num_images_label = tk.Label(camera_frame, text="Enter Number of Images:").grid(row=6,column=0, padx=1,pady=1 )
num_images_entry = tk.Entry(camera_frame)
num_images_entry.grid(row=6,column=1, padx=1,pady=1 )
num_images_entry.bind("<KeyRelease>", set_image_number)
capture_calibration_button = tk.Button(camera_frame, text="Capture Calibration Images", command=capture_calibration_images).grid(row=9,column=0,padx=1,pady=1)


# Start GUI
root.mainloop()


     