from tkinter import *

def update_variable(steps):
    value = steps_entry.get()  # Get the text from the Entry widget
    # Do something with the value
    print("The entered value is:", value)
# Set the step speed
def set_step_speed(speed):
    global step_speed
    step_speed = speed_scale.get()

root = Tk()
root.title("Control For Optode Platform")
root.config(bg="orange")

main_frame = Frame(root, width=200, height=400)
main_frame.grid(row=1, column=0,padx=10,pady=5)

exit_button = Button(root, text="Exit").grid(row=2,column=0,padx=1,pady=1)

#Preview Function#
preview_frame= Frame(root,width=200,height=100)
preview_frame.grid(row=0,column=0,padx=5,pady=5)

# Button to start the camera preview
preview_button = Button(preview_frame, text="Start Live Preview")
preview_button.pack()

# Button to stop the camera preview
stop_preview_button = Button(preview_frame,text="Stop Live Preview")
stop_preview_button.pack()


#Manual motor control Frame
motor_control=Frame(main_frame,width=100,height=185)
motor_control.grid(row=2,column=0, padx=5, pady=5)
Label(main_frame,text="Manual Motor Control").grid(row=1,column=0,padx=5,pady=5)

# Set Step Speed
speed_label = Label(motor_control, text="Step Speed Control:").grid(row=1,column=0,padx=1,pady=1)
speed_scale = Scale(motor_control, from_=0.0001, to=0.0005, resolution=0.0001, orient=HORIZONTAL)
speed_scale.configure(length=200)
speed_scale.grid(row=1,column=1,padx=1,pady=1)
speed_scale.bind("<ButtonRelease-1>", set_step_speed)

# Create the vertical motor control frame
vertical_label = Label(motor_control, text="Move Vertical:").grid(row=2,column=0,padx=0,pady=0)
vertical_direction_button = Button(motor_control, text="Down").grid(row=2,column=1,padx=1,pady=1)
vertical_direction_button = Button(motor_control, text="Up").grid(row=2,column=2,padx=1,pady=1)
steps_label = Label(motor_control, text="Steps: ").grid(row=2,column=3,padx=1,pady=1)
steps_entry = Entry(motor_control)
steps_entry.grid(row=2,column=4,padx=1,pady=1)
steps_entry.bind("<KeyRelease>", update_variable)

# Create the rotate motor control frame
horizontal_label = Label(motor_control, text="Move Horizontal:").grid(row=3,column=0,padx=0,pady=0)
horizontal_direction_button = Button(motor_control, text="Left").grid(row=3,column=1,padx=1,pady=1)
horizontal_direction_button = Button(motor_control, text="Right").grid(row=3,column=2,padx=1,pady=1)
horizontal_steps_label = Label(motor_control, text="Steps: ").grid(row=3,column=3,padx=1,pady=1)
horizontal_steps_entry = Entry(motor_control)
horizontal_steps_entry.grid(row=3,column=4,padx=1,pady=1)
horizontal_steps_entry.bind("<KeyRelease>", update_variable)

# Distance Sensor
distance_label = Label(motor_control, text="Distance from Bottom: ")
distance_label.grid(row=4,column=0,padx=1,pady=1)


# Temperature and humidity 
temp_humid_frame = Frame(main_frame,width=100,height=100)
temp_humid_frame.grid(row=5,column=1,padx=1,pady=1)

temp_label = Label(temp_humid_frame, text="Temperature:").grid(row=1,column=1,padx=1,pady=1)
temp_value = Label(temp_humid_frame, text="-").grid(row=1,column=2,padx=1,pady=1)
humidity_label = Label(temp_humid_frame, text="Humidity:").grid(row=1,column=3,padx=1,pady=1)
humidity_value = Label(temp_humid_frame, text="-").grid(row=1,column=4,padx=1,pady=1)
start_button = Button(temp_humid_frame, text="Start Temperature/humidity sensor (internal)").grid(row=1,column=0,padx=1,pady=1)



# Start GUI
root.mainloop()