import sys
import customtkinter as ctk
from tkinter import filedialog
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Button")
        
        self.button = ctk.CTkButton(self, text = "Upload WAV File", command = self.button_click)
        self.button.grid(row = 0, column = 0, padx=175, pady=200)
        
    def button_click(self):
        file_path = filedialog.askopenfilename(title="Open Wav File", initialdir="/", filetypes=[("Open Wav File", "*.wav")])
        
        sample_rate, data = wavfile.read(file_path)
        print(f"Number of channels: {data.shape[1]}")
        length_seconds = data.shape[0] / sample_rate
        print(f"Length: {length_seconds:.2f} seconds")
        left_max = np.max(np.absolute(data[:,0]))
        right_max = np.max(np.absolute(data[:,1]))
        left_avg = np.average(np.absolute(data[:,0]), axis=None,
            weights=None, returned=False)
        right_avg = np.average(np.absolute(data[:,1]), axis=None,
            weights=None, returned=False)

        print(f"Max Amplitude Left: {self.ampToDecibel(left_max):.2f} dB")
        print(f"Max Amplitude Right: {self.ampToDecibel(right_max):.2f} dB")

        print(f"Avg. Amplitude Left: {self.ampToDecibel(left_avg):.2f} dB")
        print(f"Avg. Amplitude Right: {self.ampToDecibel(right_avg):.2f} dB")
        
        time = np.linspace(0., length_seconds, data.shape[0])
        fig, (left, right) = plt.subplots(2,1,figsize=(8,6))
        left.plot(time, data[:,0], label="Left channel")
        right.plot(time, data[:,1], label="Right channel", color="orange")
        
        left.set_xlabel("Time [s]")
        right.set_xlabel("Time [s]")
        left.set_ylabel("Amplitude")
        right.set_ylabel("Amplitude")
        
        left.set_title("Waveform of Left Channel")
        right.set_title("Waveform of Right Channel")
        left.legend()
        right.legend()
        
        plt.tight_layout()
        plt.show()

    def ampToDecibel(self, value: float):
        normalAmp = value / 32767
        db = 20 * np.log10(normalAmp)
        return db


app = App()
app.mainloop()