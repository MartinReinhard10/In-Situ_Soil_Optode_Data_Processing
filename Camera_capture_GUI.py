import tkinter as tk
import time
import numpy as np
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform

class CameraGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.picam2 = None

    def create_widgets(self):
        # ExposureTime label and input box
        self.exposure_label = tk.Label(self, text="Exposure Time (us): ")
        self.exposure_label.pack(side="top")
        self.exposure_input = tk.Entry(self)
        self.exposure_input.pack(side="top")

        # AnalogueGain label and input box
        self.gain_label = tk.Label(self, text="Analogue Gain: ")
        self.gain_label.pack(side="top")
        self.gain_input = tk.Entry(self)
        self.gain_input.pack(side="top")

        # Button to take an image
        self.capture_button = tk.Button(self, text="Capture", command=self.capture_image)
        self.capture_button.pack(side="top")

        # Button to start the camera preview
        self.preview_button = tk.Button(self, text="Preview", command=self.start_preview)
        self.preview_button.pack(side="top")

        # Button to stop the camera preview
        self.stop_preview_button = tk.Button(self, text="Stop Preview", command=self.stop_preview)
        self.stop_preview_button.pack(side="top")

        # Button to exit the program
        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(side="bottom")

    def start_preview(self):
        # Create the Picamera2 instance and start the preview
        self.picam2 = Picamera2()
        self.picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
        self.picam2.start()

    def stop_preview(self):
        # Stop the camera preview
        self.picam2.stop_preview()
        self.picam2.close()

    def capture_image(self):
        # Get the exposure time and analogue gain from the input boxes
        exposure_time = int(self.exposure_input.get())
        gain = float(self.gain_input.get())

        # Set camera controls
        controls = {"ExposureTime": exposure_time,  # microseconds
                    "AnalogueGain": gain,  # 1 = ISO 100
                    "AeEnable": False,  # Auto exposure and Gain
                    "AwbEnable": False,  # Auto white Balance
                    "FrameDurationLimits": (114, 239000000)}  # Min/Max frame duration

        # Setup config parameters
        preview_config = self.picam2.create_preview_configuration(raw={"size": self.picam2.sensor_resolution, "format": "SBGGR12", },
                                                         controls=controls)
        self.picam2.configure(preview_config)
        
        picam2.start() # Start Camera
 
        time.sleep(3)

        # Capture image in unpacked RAW format 12bit dynamic range (16bit dataframe)
        raw = self.picam2.capture_array("raw").view(np.uint16)

        print(self.picam2.stream_configuration("raw"))
        print(self.picam2.capture_metadata())

    def quit(self):
        # Stop the camera preview and exit the program
        if self.picam2 is not None:
            self.picam2.stop_preview()
            self.picam2.close()
        self.master.destroy()

# Create the GUI window
root = tk.Tk()
app = CameraGUI(master=root)
app.mainloop()
