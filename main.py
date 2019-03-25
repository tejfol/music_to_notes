# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from pydub import AudioSegment
from math import log2, pow
from recordSound import record_sound as rec
import os


# showing the window
root = Tk()

# Using 'stringvar' to update label
v = StringVar()
mjaw = Label(root, textvariable=v, font=('', 50))
mjaw.place(x=60, y=150)

# loaded file inputted
lbl1 = Label(root)
lbl1.place(x=15, y=100)

# The start button


def start():
    x = lbl1['text']
    # converting the record to mono! file

    if x == "":
        messagebox.showwarning("File Missing", "Open a file first.")
    else:
        sound = AudioSegment.from_wav(x)
        sound = sound.set_channels(1)
        sound.export(x, format="wav")
        main(x)


# record the music
def record():
    # WE WILL WRITE SOME CONDITIONS HERE
    rec()
    lbl1.configure(text=os.path.dirname(
        os.path.abspath(__file__)) + "/myRecord.wav")
    # Openfile dialog


def OpenFile():
    name = askopenfilename(initialdir="/",
                           filetypes=(("Text File", "*.wav"),
                                      ("All Files", "*.*")),
                           title="Choose a file."
                           )
    if not name:
        return name
# Converting stere music to mono!
    sound = AudioSegment.from_wav(name)
    sound = sound.set_channels(1)
    sound.export(name, format="wav")
# Using try in case user types in unknown file or closes without choosing a file.
    try:
        lbl1.config(text=str(name))
    except:
        lbl1.config(text="File not exist")


# Imported images
startimg = PhotoImage(file="img/but.png")
openfileimg = PhotoImage(file="img/openfile.png")
recordimg = PhotoImage(file="img/record.png")
# Start the process Button
startBtn = Button(root, text="Start", image=startimg,
                  width="80", height="20", command=start)
startBtn.place(x=15, y=15)
# Opening files Button
openfileBtn = Button(root, text='Open file',
                     image=openfileimg, command=OpenFile)
openfileBtn.place(x=15, y=45)
# Stop Button
recordBtn = Button(root, text="Record", image=recordimg, command=record)
recordBtn.place(x=15, y=75)


# The frequency
A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def matching_thefreq(thefreq):
    # DISABLE BUTTONS WHILE SOMETHING HAPPENING
    startBtn.config(state=DISABLED)
    openfileBtn.config(state=DISABLED)
    recordBtn.config(state=DISABLED)
    h = round(12 * log2(thefreq / C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


'''---> old frequency searcher --->def matching_thefreq(thefreq):
    note = ""
    if(thefreq > 15 and thefreq < 17.32):
        note = "C0"
        return note
    elif(thefreq > 17.32 and thefreq < 19.45):
        note = "D0"
        return note
    elif(thefreq > 19.45 and thefreq < 20.8):
        note = "E0"
        return note
    elif(thefreq > 20.8 and thefreq < 23.12):
        note = "F0"
        return note
    elif(thefreq > 23.12 and thefreq < 25.96):
        note = "G0"
        return note
    elif(thefreq > 25.96 and thefreq < 29.14):
        note = "A0"
        return note
    elif(thefreq > 29.14 and thefreq < 31):
        note = "B0"
        return note
    elif(thefreq > 31 and thefreq < 34.65):
        note = "C1"
        return note
    elif(thefreq > 34.65 and thefreq < 38.89):
        note = "D1"
        return note
    elif(thefreq > 38.89 and thefreq < 42):
        note = "E1"
        return note
    elif(thefreq > 42 and thefreq < 46.25):
        note = "F1"
        return note
    elif(thefreq > 46.25 and thefreq < 51.91):
        note = "G1"
        return note
    elif(thefreq > 51.91 and thefreq < 58.27):
        note = "A1"
        return note
    elif(thefreq > 58.27 and thefreq < 63):
        note = "B1"
        return note
    elif(thefreq > 63 and thefreq < 69.30):
        note = "C2"
        return note
    elif(thefreq > 69.30 and thefreq < 77.78):
        note = "D2"
        return note
    elif(thefreq > 77.78 and thefreq < 85):
        note = "E2"
        return note
    elif(thefreq > 85 and thefreq < 92.50):
        note = "F2"
        return note
    elif(thefreq > 92.50 and thefreq < 103.83):
        note = "G2"
        return note
    elif(thefreq > 103.83 and thefreq < 116.54):
        note = "A2"
        return note
    elif(thefreq > 116.54 and thefreq < 126):
        note = "B2"
        return note
    elif(thefreq > 126 and thefreq < 138.59):
        note = "C3"
        return note
    elif(thefreq > 138.59 and thefreq < 155.56):
        note = "D3"
        return note
    elif(thefreq > 155.56 and thefreq < 168):
        note = "E3"
        return note
    elif(thefreq > 168 and thefreq < 185):
        note = "F3"
        return note
    elif(thefreq > 185 and thefreq < 207.65):
        note = "G3"
        return note
    elif(thefreq > 207.65 and thefreq < 233.08):
        note = "A3"
        return note
    elif(thefreq > 233.08 and thefreq < 253):
        note = "B3"
        return note
    elif(thefreq > 253 and thefreq < 277.18):
        note = "C4"
        return note
    elif(thefreq > 277.18 and thefreq < 311.13):
        note = "D4"
        return note
    elif(thefreq > 311.13 and thefreq < 338):
        note = "E4"
        return note
    elif(thefreq > 338 and thefreq < 369.99):
        note = "F4"
        return note
    elif(thefreq > 369.99 and thefreq < 415.3):
        note = "G4"
        return note
    elif(thefreq > 415.3 and thefreq < 466.16):
        note = "A4"
        return note
    elif(thefreq > 466.16 and thefreq < 500):
        note = "B4"
        return note
    elif(thefreq > 500 and thefreq < 554.37):
        note = "C5"
        return note
    elif(thefreq > 554.37 and thefreq < 622.25):
        note = "D5"
        return note
    elif(thefreq > 622.25 and thefreq < 675):
        note = "E5"
        return note
    elif(thefreq > 675 and thefreq < 740):
        note = "F5"
        return note
    elif(thefreq > 740 and thefreq < 830):
        note = "G5"
        return note
    elif(thefreq > 830 and thefreq < 932):
        note = "A5"
        return note
    elif(thefreq > 932 and thefreq < 1000):
        note = "B5"
        return note
    elif(thefreq > 1000 and thefreq < 1108):
        note = "C6"
        return note
    elif(thefreq > 1108 and thefreq < 1244):
        note = "D6"
        return note
    elif(thefreq > 1244 and thefreq < 1350):
        note = "E6"
        return note
    elif(thefreq > 1350 and thefreq < 1480):
        note = "F6"
        return note
    elif(thefreq > 1480 and thefreq < 1661.22):
        note = "G6"
        return note
    elif(thefreq > 1661.22 and thefreq < 1864):
        note = "A6"
        return note
    elif(thefreq > 1864 and thefreq < 2000):
        note = "B6"
        return note
    elif(thefreq > 2000 and thefreq < 2217.46):
        note = "C7"
        return note
    elif(thefreq > 2217.46 and thefreq < 2489.02):
        note = "D7"
        return note
    elif(thefreq > 2489.02 and thefreq < 2700):
        note = "E7"
        return note
    elif(thefreq > 2700 and thefreq < 2960):
        note = "F7"
        return note
    elif(thefreq > 2960 and thefreq < 3322.4):
        note = "G7"
        return note
    elif(thefreq > 3322.4 and thefreq < 3729):
        note = "A7"
        return note
    elif(thefreq > 3729.31 and thefreq < 4040):
        note = "B7"
        return note
    elif(thefreq > 4040 and thefreq < 4435):
        note = "C8"
        return note
    elif(thefreq > 4435 and thefreq < 4978):
        note = "D8"
        return note
    elif(thefreq > 4978 and thefreq < 5350):
        note = "E8"
        return note
    elif(thefreq > 5350 and thefreq < 5919):
        note = "F8"
        return note
    elif(thefreq > 5919 and thefreq < 6644):
        note = "G8"
        return note
    elif(thefreq > 6644 and thefreq < 7458):
        note = "A8"
        return note
    elif(thefreq > 7458 and thefreq < 8000):
        note = "B8"
        return note'''


# THE MAIN WIZARD WHO MAKING THE MAGIC (*_*)
def main(sound):
    chunk = 2048

    # open up a wave
    wf = wave.open(sound, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=RATE,
                    output=True)

    # read some data
    data = wf.readframes(chunk)
    # play stream and find the frequency of each chunk
    while len(data) == chunk * swidth:
        # write data out to the audio stream
        stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth),
                                             data)) * window
        # Take the fft and square each value
        fftData = abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which + x1) * RATE / chunk
            # print ("The freq is %f Hz." % (thefreq))                   #printing out the frequency
            v.set(str(matching_thefreq(thefreq)))
            lbl1.update()
            
            
            
        else:
            thefreq = which * RATE / chunk
            # print ("The freq is %f Hz." % (thefreq))
            v.set(str(matching_thefreq(thefreq)))
            lbl1.update()

        # read some more data
        data = wf.readframes(chunk)
    if data:
        stream.write(data)
        startBtn.config(state=NORMAL)
        openfileBtn.config(state=NORMAL)
        recordBtn.config(state=NORMAL)

    stream.close()
    p.terminate()


root.geometry("720x480")
root.title("Welcome")
root.mainloop()
