import tkinter as tk
import Live_Camera_Preview as LCP
import Motor_Function as mf



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
preview_button = tk.Button(preview_frame, text="Start Live Preview", command= LCP.start_preview)
preview_button.pack()

# Button to stop the camera preview
stop_preview_button = tk.Button(preview_frame,text="Stop Live Preview", command=LCP.stop_preview)
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

# Start GUI
root.mainloop()