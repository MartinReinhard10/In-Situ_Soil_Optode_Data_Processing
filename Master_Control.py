import tkinter as tk
import subprocess

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("GUI")

        self.button = tk.Button(master, text="Execute Script", command=self.execute_script)
        self.button.pack()

    def execute_script(self):
        subprocess.call(['python', '/home/martin/Desktop/Scripts/Sensor_Calibration.py'])

root = tk.Tk()
gui = GUI(root)
root.mainloop()
