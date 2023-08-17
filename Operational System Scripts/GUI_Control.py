import time
import tkinter as tk
import Camera_Function as cf
import Motor_Function as mf
import Distance_sensor_Function as dsf
import Temp_Humid_Function as thf
import Measurement_Functions as mefu

# EXIT GUI Command
def exit_app():
        thf.dhtDevice.exit()
        root.destroy()
        cf.GPIO.cleanup(25)

# GUI Layout and function
root = tk.Tk()
root.title("Control For Optode Platform")

main_frame = tk.Frame(root, width=1000, height=1000)
main_frame.grid(row=0, column=0,padx=20,pady=20)

exit_button = tk.Button(main_frame, text="Exit", fg="red", font=("Arial",20), command=exit_app).grid(row=1,column=5,padx=5,pady=5)

# Message window
def display_message(message):
    text_widget.insert('end', message + '\n')
    text_widget.see('end')  # Auto-scroll to the end

#text_widget_label = tk.Label(main_frame, text= "System Messages:", font="Arial").grid(row=0,column=4,padx=5,pady=5)
text_widget = tk.Text(main_frame, height=20, width=20)
text_widget.grid(row=1, column=4, padx=2, pady=5)

#Manual motor control Frame
motor_control=tk.Frame(main_frame,width=500,height=500)
motor_control.grid(row=1,column=1, padx=10, pady=10)
#tk.Label(main_frame,text="Manual Motor Controls:", font="Arial").grid(row=0,column=1,padx=5,pady=5)

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
vertical_direction_button = tk.Button(motor_control, text="Down", command=lambda: mf.move_vertical_DOWN(mf.num_steps_vertical)).grid(row=4,column=0,padx=1,pady=1)
vertical_direction_button = tk.Button(motor_control, text="Up", command=lambda: mf.move_vertical_UP(mf.num_steps_vertical)).grid(row=4,column=1,padx=1,pady=1)
vertical_steps_label = tk.Label(motor_control, text="Vertical Steps: ").grid(row=2,column=0,padx=10,pady=10)
vertical_steps_entry = tk.Entry(motor_control)
vertical_steps_entry.grid(row=2,column=1,padx=1,pady=1)
vertical_steps_entry.bind("<KeyRelease>", set_steps_vertical)

# Create the rotate motor control frame
def set_steps_horizontal(steps_h):
    mf.set_steps_horizontal(horizontal_steps_entry.get())
horizontal_direction_button = tk.Button(motor_control, text="Left", command=lambda:mf.rotate_LEFT(mf.num_steps_horizontal)).grid(row=5,column=0,padx=1,pady=1)
horizontal_direction_button = tk.Button(motor_control, text="Right", command=lambda: mf.rotate_RIGHT(mf.num_steps_horizontal)).grid(row=5,column=1,padx=1,pady=1)
horizontal_steps_label = tk.Label(motor_control, text=" Horizontal Steps: ").grid(row=3,column=0,padx=10,pady=10)
horizontal_steps_entry = tk.Entry(motor_control)
horizontal_steps_entry.grid(row=3,column=1,padx=1,pady=1)
horizontal_steps_entry.bind("<KeyRelease>", set_steps_horizontal)

#Move "HOME" 
home_button = tk.Button(motor_control, text="Move to Bottom Position", command=mf.move_home).grid(row=6,column=0,padx=10,pady=10)

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
distance_label.grid(row=8,column=0,padx=10,pady=10)
dsf.measure_distance(distance_label)

# Temperature and humidity 
temp_humid_frame = tk.Frame(main_frame,width=100,height=100)
temp_humid_frame.grid(row=5,column=4,padx=1,pady=1)
temp_label = tk.Label(temp_humid_frame, text="Temperature:")
temp_label.grid(row=1,column=1,padx=1,pady=1)
humidity_label = tk.Label(temp_humid_frame, text="Humidity:")
humidity_label.grid(row=1,column=4,padx=1,pady=1)
thf.update_temp_values(temp_label, humidity_label)

# Camera functions
camera_frame = tk.Frame(main_frame, width=200,height=500)
camera_frame.grid(row=1,column=2,padx=10,pady=10)
#camera_frame_title = tk.Label(main_frame, text= "Camera Functions:",font="Arial").grid(row=0,column=2,padx=5,pady=5)
preview_button = tk.Button(camera_frame, text="Start Live Preview", command=cf.start_preview).grid(row=1,column=0,padx=5,pady=5)
stop_preview_button = tk.Button(camera_frame,text="Stop Live Preview", command=cf.stop_preview).grid(row=1,column=1,padx=5,pady=5)
camera_jpeg_button = tk.Button(camera_frame, text="Capture JPEG Image", command= cf.capture_jpeg).grid(row=2,column=0,padx=5,pady=5)
camera_raw_button = tk.Button(camera_frame, text="Capture RAW Image", command=lambda: cf.capture_raw(uv_state, exposure_time, iso_value)).grid(row=6,column=0,padx=1,pady=1)


# Camera Settings: Exposure and ISO
def set_exposure(exposure):
     global exposure_time
     exposure_time_get = exposure_entry.get() 
     exposure_time = int(float(exposure_time_get) * 10E5)
     display_message(f"exposure: {exposure_time}\n")
     

exposure_label = tk.Label(camera_frame, text= "Exposure Time (seconds):").grid(row=3,column=0,padx=1,pady=1)     
exposure_entry = tk.Entry(camera_frame)
exposure_entry.grid(row=3,column=1,padx=1,pady=1)
exposure_entry.bind("<KeyRelease>", set_exposure)

def set_iso(iso):
     global iso_value
     iso_value_get = iso_entry.get()
     iso_value = int(iso_value_get)
     display_message(f"ISO: {iso_value}\n")

iso_label = tk.Label(camera_frame, text= "ISO:").grid(row=4,column=0,padx=1,pady=1)
iso_entry = tk.Entry(camera_frame)
iso_entry.grid(row=4,column=1,padx=1,pady=1)
iso_entry.bind("<KeyRelease>", set_iso)

#UV LED Control
def toggle_uv_state():
    global uv_state
    if uv_label.cget("text") == "ON":
        uv_label.config(text="OFF")
        cf.GPIO.output(cf.led, cf.GPIO.LOW)
    else:
        uv_label.config(text="ON")
        #cf.GPIO.output(cf.led, cf.GPIO.HIGH)
    
    uv_state = uv_label.cget("text") == "ON"

    display_message(f"UV state: {uv_state}\n")
    
uv_label = tk.Label(camera_frame,text="OFF")
uv_label.grid(row=6,column=1,padx=5,pady=5)
uv_button =tk.Button(camera_frame,text="Toggle UV LED:", command=toggle_uv_state).grid(row=5,column=0,padx=5,pady=5)

#White LED Control
def toggle_white_led_state():
    global white_state
    if white_label.cget("text") == "ON":
        white_label.config(text="OFF")
        cf.GPIO.output(cf.white_led, cf.GPIO.LOW)
    else:
        white_label.config(text="ON")
        cf.GPIO.output(25,cf.GPIO.HIGH)
    
    white_state = white_label.cget("text") == "ON"

    display_message(f"White LED state: {white_state}\n")
    
white_label = tk.Label(camera_frame,text="OFF")
white_label.grid(row=0,column=1,padx=5,pady=5)
white_button =tk.Button(camera_frame,text="Toggle White LED:", command=toggle_white_led_state).grid(row=0,column=0,padx=5,pady=5)

#Show Histogram 
histogram_button = tk.Button(camera_frame, text= "RAW Channels Histogram", command=cf.display_histogram).grid(row=6,column=1, padx=1,pady=1 )

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
    display_message("Image Sequence Completed.\n")

o2_label = tk.Label(camera_frame, text="Set Image Name:").grid(row=10,column=0,padx=1,pady=1)
o2_entry = tk.Entry(camera_frame)
o2_entry.grid(row=10,column=1,padx=1,pady=1)
o2_entry.bind("<KeyRelease>", set_o2)
delay_time_label = tk.Label(camera_frame, text="Set Delay Between Images:").grid(row=9,column=0,padx=1,pady=1)
delay_time_entry = tk.Entry(camera_frame)
delay_time_entry.grid(row=9,column=1,padx=1,pady=1)
delay_time_entry.bind("<KeyRelease>", set_delay)
num_images_label = tk.Label(camera_frame, text="Enter Number of Images:").grid(row=8,column=0, padx=1,pady=1 )
num_images_entry = tk.Entry(camera_frame)
num_images_entry.grid(row=8,column=1, padx=1,pady=1 )
num_images_entry.bind("<KeyRelease>", set_image_number)
capture_calibration_button = tk.Button(camera_frame, text="Capture Image Sequence", command=capture_calibration_images).grid(row=11,column=0,padx=10,pady=10)
capture_calibration_label = tk.Label(camera_frame,text="Sequence Settings:", font=8).grid(row=7,column=0,padx=10,pady=10)


#Measurements Sequence

#Camera field of view in cm
fov_x = 3.3 
fov_y = 2.5
#Camera field of view in steps
fov_x_steps = round(fov_x * 407.5)
fov_y_steps = round(fov_y * 800)

def measurement_direction():
    global direction
    if measurement_direction_vertical_label.cget("text") == "UP":
       measurement_direction_vertical_label.config(text="DOWN")
       direction = False
    else:
       measurement_direction_vertical_label.config(text="UP")
       direction = True

    message = f"Direction_state: {direction}\n"
    text_widget.insert('end', message)
    text_widget.see('end')

def set_horizontal_step_range(hori_range_trigger):
    global hori_range
    hori_range_get = int(horizontal_view_entry.get())
    if hori_range_get < 1:
        message = f"Horizontal range must be at least 1\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif hori_range_get == 1:
        hori_range = 0 
        message = f"Horizontal Step Range: {hori_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        hori_range = round(hori_range_get * fov_x_steps)
        message = f"Horizontal Step Range: {hori_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
     
def set_verticale_step_range(vert_range_trigger):
    global vert_range
    vert_range_get = int(vertical_view_entry.get())
    if vert_range_get < 1:
        message = f"Vertical range must be at least 1\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif vert_range_get ==1:
        vert_range = 0
        message = f"Vertical Step Range: {vert_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        vert_range = round(vert_range_get * fov_y_steps)
        message = f"Vertical Step Range: {vert_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')


def set_horizontal_overlap(hori_overlap_trigger):
    global hori_overlap
    hori_overlap_get = int(horizontal_overlap_entry.get())
    if hori_overlap_get > 99:
        message = f"Maximum 99% overlap\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif hori_overlap_get == 0:
        hori_overlap = fov_x_steps
        message = f"Horizontal Step Overlap: {hori_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        hori_overlap = round((100-hori_range) * hori_overlap_get / 100)
        message = f"Horizontal Step Overlap: {hori_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')

def set_vertical_overlap(vert_overlap_trigger):
    global vert_overlap
    vert_overlap_get = int(vertical_overlap_entry.get())
    if vert_overlap_get > 99:
        message = f"Maximum 99% overlap\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif vert_overlap_get == 0:
        vert_overlap = fov_y_steps
        message = f"vertical Step Overlap: {vert_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        vert_overlap = round((100-vert_range) * vert_overlap_get / 100)
        message = f"Vertical Step Overlap: {vert_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')

def image_range():
    global hori_image_range
    global vert_image_range
    global num_images_seq
    hori_image_range = round(hori_range/hori_overlap)
    vert_image_range = round(vert_range/vert_overlap)
    num_images_seq = round(hori_image_range * vert_image_range)
    number_images_sequence.config(text="Number of Images in Sequence: {}".format(num_images_seq))
    print(hori_image_range)
    print(vert_image_range)

def set_seqeunce_number(seq_num_trigger):
    global seq_num
    seq_num = int(sequence_number_entry.get())



# Add a variable to track the number of times the sequence has run
sequence_count = 0

# Function to execute the measurement sequence
def run_measurement_sequence():
    global sequence_count

     # Get the total number of sequences and sequence delay from the input fields
    total_sequences = int(total_sequences_entry.get())
    sequence_delay = int(sequence_delay_entry.get())

    # Run the measurement sequence logic
    mefu.measurement_sequence(vert_image_range, hori_image_range, vert_overlap, hori_overlap, direction, exposure_time, iso_value, uv_state, seq_num)
    
    # Call the function to move the camera back to initial position
    mefu.move_to_initial_position(vert_image_range, hori_image_range, direction)

    # Increment the sequence count
    sequence_count += 1
    message = f"Completed sequence {sequence_count}\n"
    text_widget.insert('end', message)
    text_widget.see('end')
    

    # Check if the desired number of sequences have run
    if sequence_count < total_sequences:
        message = f"Waiting for {sequence_delay} seconds before starting the next sequence...\n"
        text_widget.insert('end', message)
        text_widget.see('end')

        time.sleep(sequence_delay)

        # Call the function recursively to run the next sequence
        run_measurement_sequence()
    else:
        message = f"All sequences completed!\n"
        text_widget.insert('end', message)
        text_widget.see('end')
        

# Function to start the measurement sequence
def start_measurement():
    global sequence_count

    # Reset sequence count before starting
    sequence_count = 0

    # Call the function to run the measurement sequence
    run_measurement_sequence()

def set_seqeunce_number(seq_num_trigger):
    global seq_num
    seq_num = int(sequence_number_entry.get())


mearsurement_frame = tk.Frame(main_frame,width=200,height=500)
mearsurement_frame.grid(row=1,column=3,padx=1,pady=1)
#mearsurement_frame_title = tk.Label(main_frame, text="Measurement Sequence:",font="Arial").grid(row=0,column=3,padx=5,pady=5)
horizontal_view_label = tk.Label(mearsurement_frame,text="Set horizontal range (cm):").grid(row=0,column=0,padx=1,pady=1)
horizontal_view_entry = tk.Entry(mearsurement_frame)
horizontal_view_entry.grid(row=0,column=1,padx=5,pady=5)
horizontal_view_entry.bind("<KeyRelease>", set_horizontal_step_range)
vertical_view_label = tk.Label(mearsurement_frame,text="Set vertical range (cm):").grid(row=1,column=0,padx=1,pady=1)
vertical_view_entry = tk.Entry(mearsurement_frame)
vertical_view_entry.grid(row=1,column=1,padx=5,pady=5)
vertical_view_entry.bind("<KeyRelease>",set_verticale_step_range)
horizontal_overlap_label = tk.Label(mearsurement_frame,text="Set Horizontal Image Overlap %:").grid(row=2,column=0,padx=1,pady=1)
horizontal_overlap_entry = tk.Entry(mearsurement_frame)
horizontal_overlap_entry.grid(row=2,column=1,padx=5,pady=5)
horizontal_overlap_entry.bind("<KeyRelease>",set_horizontal_overlap)
vertical_overlap_label = tk.Label(mearsurement_frame,text="Set Vertical Image Overlap %:").grid(row=3,column=0,padx=1,pady=1)
vertical_overlap_entry = tk.Entry(mearsurement_frame)
vertical_overlap_entry.grid(row=3,column=1,padx=5,pady=5)
vertical_overlap_entry.bind("<KeyRelease>", set_vertical_overlap)
measurement_direction_vertical_label = tk.Label(mearsurement_frame, text="DOWN")
measurement_direction_vertical_label.grid(row=4,column=1,padx=5,pady=5)
measurement_direction_vertical_button = tk.Button(mearsurement_frame,text="Vertical Measurement Direction:", command=measurement_direction).grid(row=4,column=0,padx=5,pady=5)
confirm_button = tk.Button(mearsurement_frame,text="Confirm Image Range", command=image_range).grid(row=5,column=0,padx=5,pady=5)
number_images_sequence = tk.Label(mearsurement_frame, text="Number of Images in Sequence:")
number_images_sequence.grid(row=6,column=0,padx=5,pady=5)
sequence_number_label = tk.Label(mearsurement_frame,text="Set Sequence Number for Archiving:").grid(row=7,column=0,padx=5,pady=5)
sequence_number_entry = tk.Entry(mearsurement_frame)
sequence_number_entry.grid(row=7,column=1,padx=5,pady=5)
sequence_number_entry.bind("<KeyRelease>", set_seqeunce_number)
start_measure_button = tk.Button(mearsurement_frame,text="Start Measurement Sequence", command=start_measurement).grid(row=8,column=0,padx=5,pady=5)
#stop_measure_button = tk.Button(mearsurement_frame,text="Stop Measurement Sequence").grid(row=8,column=1,padx=5,pady=5)

# Add input fields for setting the total number of sequences and delay between sequences
total_sequences_label = tk.Label(mearsurement_frame, text="Total Number of Sequences:")
total_sequences_label.grid(row=10, column=0, padx=5, pady=5)
total_sequences_entry = tk.Entry(mearsurement_frame)
total_sequences_entry.grid(row=10, column=1, padx=5, pady=5)

sequence_delay_label = tk.Label(mearsurement_frame, text="Delay Between Sequences (seconds):")
sequence_delay_label.grid(row=11, column=0, padx=5, pady=5)
sequence_delay_entry = tk.Entry(mearsurement_frame)
sequence_delay_entry.grid(row=11, column=1, padx=5, pady=5)

# Start GUI
root.mainloop()


     