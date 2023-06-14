import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep

led = 23

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.led_on_button = tk.Button(self)
        self.led_on_button["text"] = "Turn LED on for 2 seconds"
        self.led_on_button["command"] = self.turn_led_on
        self.led_on_button.pack(side="top")

        self.quit_button = tk.Button(self, text="Quit", fg="red",
                              command=self.master.destroy)
        self.quit_button.pack(side="bottom")

    def turn_led_on(self):
        #SETUP:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led, GPIO.OUT)

        #ACTIVE FOR TWO SEC.
        GPIO.output(led, GPIO.HIGH)

        sleep(5)

        GPIO.output(led, GPIO.LOW)

        GPIO.cleanup()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
