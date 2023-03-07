import time
import tkinter as tk
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D8)

class DHT22App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("DHT22 Sensor GUI")
        
        # Create widgets
        self.temp_label = tk.Label(self, text="Temperature:")
        self.temp_value = tk.Label(self, text="-")
        self.humidity_label = tk.Label(self, text="Humidity:")
        self.humidity_value = tk.Label(self, text="-")
        self.start_button = tk.Button(self, text="Start", command=self.start_measurement)
        self.exit_button = tk.Button(self, text="Exit", command=self.exit_app)
        
        # Add widgets to layout
        self.temp_label.grid(row=0, column=0, padx=10, pady=10)
        self.temp_value.grid(row=0, column=1, padx=10, pady=10)
        self.humidity_label.grid(row=1, column=0, padx=10, pady=10)
        self.humidity_value.grid(row=1, column=1, padx=10, pady=10)
        self.start_button.grid(row=2, column=0, padx=10, pady=10)
        self.exit_button.grid(row=2, column=1, padx=10, pady=10)
        
        # Set initial state
        self.is_measuring = False
        self.update_values()
        
    def start_measurement(self):
        self.is_measuring = True
        self.update_values()
        
    def update_values(self):
        if self.is_measuring:
            try:
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = dhtDevice.humidity
                self.temp_value.config(text="{:.1f} F / {:.1f} C".format(temperature_f, temperature_c))
                self.humidity_value.config(text="{}%".format(humidity))
            except RuntimeError as error:
                self.temp_value.config(text="-")
                self.humidity_value.config(text="-")
                print(error.args[0])
        else:
            self.temp_value.config(text="-")
            self.humidity_value.config(text="-")
    
        # Update every 2 seconds
        self.after(2000, self.update_values)
    
    def exit_app(self):
        dhtDevice.exit()
        self.destroy()

if __name__ == "__main__":
    app = DHT22App()
    app.mainloop()
