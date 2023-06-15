import tkinter as tk
from PIL import ImageTk, Image
from picamera2 import Picamera2
import time

picam2 = Picamera2()
def capture_jpeg():
    camera_config = picam2.create_still_configuration(main={"size": (4056, 3040)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(3)
    image = picam2.capture_file()
    return image

def capture_and_display():
    # Capture the JPEG image
    image_path = capture_jpeg()

    # Open the image using PIL
    pil_image = Image.open(image_path)

    # Convert the PIL image to Tkinter-compatible format
    tk_image = ImageTk.PhotoImage(pil_image)

    # Update the image on the label
    label.configure(image=tk_image)
    label.image = tk_image

# Create the GUI
root = tk.Tk()
root.title("Capture and Display")

image_frame = tk.Frame(root, width=500, height=500)
image_frame.pack()

# Create a Label Widget to display the image
label = tk.Label(image_frame)
label.pack()

# Create a Button to trigger the capture function
capture_button = tk.Button(root, text="Capture", command=capture_and_display)
capture_button.pack()

# Start the GUI
root.mainloop()
