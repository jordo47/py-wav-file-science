import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

class App(tk.Tk):
    #initialize root window of app
    def __init__(self):
        super().__init__()
        self.geometry("250x250")
        self.title("Select a File...")
        
        #create button and event for button click,, attach to root window
        self.button = tk.ttk.Button(self, text = "Upload WAV File", command = self.button_click)
        self.button.grid(row = 0, column = 0, padx=75, pady=100)
        
    def button_click(self):
        #open file dialog, restricted to wav files
        file_path = filedialog.askopenfilename(title="Open Wav File", initialdir="/", 
            filetypes=[("Open Wav File", "*.wav")])

        #read wav file
        sample_rate, data = wavfile.read(file_path)
        isStereo = len(data.shape) - 1

        length_seconds = data.shape[0] / sample_rate
        print(f"Length: {length_seconds:.2f} seconds")
        
        #find max and avg. amplitudes for each channel
        
        if isStereo:
            left_max = np.max(np.absolute(data[:,0]))
            right_max = np.max(np.absolute(data[:,1]))
        else:
            left_max = np.max(np.absolute(data[:]))
            right_max = 0
        
        if isStereo:
            left_avg = np.average(np.absolute(data[:,0]), axis=None,
                weights=None, returned=False)
            right_avg = np.average(np.absolute(data[:,1]), axis=None,
                weights=None, returned=False)
        else:
            left_avg = np.average(np.absolute(data[:]), axis=None,
                weights=None, returned=False)
            right_avg = 0

        #create song details window
        self.showData(os.path.basename(file_path), length_seconds, left_max, right_max,
            left_avg, right_avg, isStereo)
        
        time = np.linspace(0., length_seconds, data.shape[0])
        
        #create matplots
        if isStereo:
            fig, (left, right) = plt.subplots(2,1,figsize=(8,6))
            left.plot(time, data[:data.shape[0],0], label="Left channel")
            right.plot(time, data[:data.shape[0],1], label="Right channel", color="orange")
        
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
        
        else:
            plt.plot(time, data[:])
            plt.title("Waveform of Mono Channel")
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            plt.legend()
            plt.tight_layout()
            plt.show()

    #convert amplitude to decibel
    def ampToDecibel(self, value: float):
        normalAmp = value / 32767
        db = 20 * np.log10(normalAmp)
        return db

    #create song details window
    def showData(self, filename: str, songLength: float, 
        maxL: float, maxR: float, avgL: float, avgR: float, isStereo: bool):

        #create window and frame
        data_w = tk.Toplevel(self)
        data_w.geometry("500x100")
        data_w.title("Song Details")

        frm = ttk.Frame(data_w, padding=10)
        frm.grid()

        #Changes label from M (mono) to L (left) if track is stereo
        isMono = "M" 
        if (isStereo == True):
            isMono = "L"

        #display file name
        ttk.Label(frm, text="Filename: ").grid(column=0, row=0)
        ttk.Label(frm, text=filename).grid(column=1, row=0)
        #display song length
        ttk.Label(frm, text="Song Length: ").grid(column=0, row=1)
        ttk.Label(frm, text=f"{songLength:.2f}s").grid(column=1, row=1)
        #display max amp as dB
        ttk.Label(frm, text="Max Amplitude: ").grid(column=0, row=2)
        ttk.Label(frm, text=isMono + f" {self.ampToDecibel(maxL):.2f} dB").grid(column=1, row=2)
        if isStereo:
            ttk.Label(frm, text=f"R {self.ampToDecibel(maxR):.2f} dB").grid(column=2, row=2)
        #display avg amp as dB
        ttk.Label(frm, text="Average Amplitude: ").grid(column=0, row=3)
        ttk.Label(frm, text=isMono + f" {self.ampToDecibel(avgL):.2f} dB").grid(column=1, row=3)
        if isStereo:
            ttk.Label(frm, text=f"R {self.ampToDecibel(avgR):.2f} dB").grid(column=2, row=3)





app = App()
app.mainloop()