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
import serial
import struct

# showing the window
root = Tk()
Identified_Notes = []
Identified_Notes2 = []
# Using 'stringvar' to update label
v = StringVar()
frequencylbl = Label(root, textvariable=v, font=('', 80))
frequencylbl.place(x=300, y=230)

# loaded file inputted
input_audio_file = Label(root)
input_audio_file.place(x=15, y=430)

# Seconds to Record
Spinbox = Spinbox(root, from_=3, to=180, width="5")
Spinbox.place(x=560, y=120)

SpinboxLbl = Label(root, text="Seconds of record:")
SpinboxLbl.place(x=425, y=120)

# The start button
def start():
    del mynotelist[:]
    x = input_audio_file['text']
    # converting the record to mono! file


    if x == "":
        messagebox.showwarning("File Missing", "Open a file first.")
    else:
        sound = AudioSegment.from_wav(x)
        sound = sound.set_channels(1)
        sound.export(x, format="wav")
        identifiNotes_ToLilypond(x)
        identifiNotes(x)
        main(x)

# remove the directory of the audio file what we choose or recorded

def removeAudio():
    if input_audio_file != "":
        input_audio_file.config(text="")
    else:
        return

# for menubar to quit the program


def quit():
    result = messagebox.askquestion('Quit', 'Are You Sure?', icon='warning')
    if result == 'yes':
        sys.exit()
    else:
        pass
# record the music


def record():
    # WE WILL WRITE SOME CONDITIONS HERE
    x = Spinbox.get()
    rec(int(x))
    input_audio_file.configure(text=os.path.dirname(
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
    name.replace(" ","_")
    
# Using try in case user types in unknown file or closes without choosing a file.
    try:
        input_audio_file.config(text=str(name))
    except:
        input_audio_file.config(text="File not exist")


# Imported images
startimg = PhotoImage(file="img/but.png")
openfileimg = PhotoImage(file="img/openfile.png")
recordimg = PhotoImage(file="img/record.png")
# Start the process Button
startBtn = Button(root, text="Start", image=startimg,
                  width="200", height="100", command=start)
startBtn.place(x=15, y=15)
# Opening files Button
openfileBtn = Button(root, text='Open file',
                     image=openfileimg, width="200", height="100", command=OpenFile)
openfileBtn.place(x=220, y=15)
# Stop Button
recordBtn = Button(root, text="Record", image=recordimg,
                   width="200", height="100", command=record)
recordBtn.place(x=425, y=15)


# The frequency
A4 = 444
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def matching_thefreq(thefreq):
    # DISABLE BUTTONS WHILE SOMETHING HAPPENING
    startBtn.config(state=DISABLED)
    openfileBtn.config(state=DISABLED)
    recordBtn.config(state=DISABLED)
    # found the ovtave
    h = round(12 * log2(thefreq / C0))
    octave = h // 12
    n = h % 12
    print(thefreq)
    return name[n] + str(octave)

#mynotelist will containe our name of the chord
mynotelist = []

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
            input_audio_file.update()


            mynotelist.append(str.lower(matching_thefreq(thefreq)))

        else:
            thefreq = which * RATE / chunk
            # print ("The freq is %f Hz." % (thefreq))
            v.set(str(matching_thefreq(thefreq)))
            input_audio_file.update()

        # read some more data
        data = wf.readframes(chunk)
    if data:
        stream.write(data)
        startBtn.config(state=NORMAL)
        openfileBtn.config(state=NORMAL)
        recordBtn.config(state=NORMAL)
    print(mynotelist)
    stream.close()
    p.terminate()

def identifiNotes(x):
    def find_nearest(array,value):
        idx = (np.abs(array-value)).argmin()
        return array[idx]

    ############################## Initialize ##################################


    # Some Useful Variables
    window_size = 2205    # Size of window to be used for detecting silence
    beta = 1   # Silence detection parameter
    max_notes = 100    # Maximum number of notes in file, for efficiency
    sampling_freq = 44100   # Sampling frequency of audio signal
    threshold = 600
    array = [1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
             2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
             4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13]

    notes = ['C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
             'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
             'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8']
    

    ############################## Read Audio File #############################
    print ('\n\nReading Audio File...')

    sound_file = wave.open(x, 'r')
    file_length = sound_file.getnframes()

    sound = np.zeros(file_length)
    mean_square = []
    sound_square = np.zeros(file_length)
    for i in range(file_length):
        data = sound_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])
        
    sound = np.divide(sound, float(2**15))  # Normalize data in range -1 to 1


    ######################### DETECTING SCILENCE ##################################

    sound_square = np.square(sound)
    frequency = []
    dft = []
    i = 0
    j = 0
    k = 0    
    # traversing sound_square array with a fixed window_size
    while(i<=len(sound_square)-window_size):
        s = 0.0
        j = 0
        while(j<=window_size):
            s = s + sound_square[i+j]
            j = j + 1   
    # detecting the silence waves
        if s < threshold:
            if(i-k>window_size*4):
                dft = np.array(dft) # applying fourier transform function
                dft = np.fft.fft(sound[k:i])
                dft=np.argsort(dft)

                if(dft[0]>dft[-1] and dft[1]>dft[-1]):
                    i_max = dft[-1]
                elif(dft[1]>dft[0] and dft[-1]>dft[0]):
                    i_max = dft[0]
                else :  
                    i_max = dft[1]
    # claculating frequency             
                frequency.append((i_max*sampling_freq)/(i-k))
                dft = []
                k = i+1
        i = i + window_size

    print('length',len(frequency))
    print("frequency")   

    for i in frequency :
        print(i)
        idx = (np.abs(array-i)).argmin()
        Identified_Notes.append(str.lower(notes[idx]))
    

def identifiNotes_ToLilypond(x):
    def find_nearest(array,value):
        idx = (np.abs(array-value)).argmin()
        return array[idx]

    ############################## Initialize ##################################


    # Some Useful Variables
    window_size = 2205    # Size of window to be used for detecting silence
    beta = 1   # Silence detection parameter
    max_notes = 100    # Maximum number of notes in file, for efficiency
    sampling_freq = 44100   # Sampling frequency of audio signal
    threshold = 600
    array = [1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
             2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
             4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13]

    notes = ['C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
             'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
             'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8']
    

    ############################## Read Audio File #############################
    print ('\n\nReading Audio File...')

    sound_file = wave.open(x, 'r')
    file_length = sound_file.getnframes()

    sound = np.zeros(file_length)
    mean_square = []
    sound_square = np.zeros(file_length)
    for i in range(file_length):
        data = sound_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])
        
    sound = np.divide(sound, float(2**15))  # Normalize data in range -1 to 1


    ######################### DETECTING SCILENCE ##################################

    sound_square = np.square(sound)
    frequency = []
    dft = []
    i = 0
    j = 0
    k = 0    
    # traversing sound_square array with a fixed window_size
    while(i<=len(sound_square)-window_size):
        s = 0.0
        j = 0
        while(j<=window_size):
            s = s + sound_square[i+j]
            j = j + 1   
    # detecting the silence waves
        if s < threshold:
            if(i-k>window_size*4):
                dft = np.array(dft) # applying fourier transform function
                dft = np.fft.fft(sound[k:i])
                dft=np.argsort(dft)

                if(dft[0]>dft[-1] and dft[1]>dft[-1]):
                    i_max = dft[-1]
                elif(dft[1]>dft[0] and dft[-1]>dft[0]):
                    i_max = dft[0]
                else :  
                    i_max = dft[1]
    # claculating frequency             
                frequency.append((i_max*sampling_freq)/(i-k))
                dft = []
                k = i+1
        i = i + window_size

    print('length',len(frequency))
    print("frequency")   

    for i in frequency :
        print(i)
        idx = (np.abs(array-i)).argmin()
        Identified_Notes2.append(str.lower(notes[idx]))



def save_file_to_lilypond():
    if len(Identified_Notes2) or len(Identified_Notes) >= 0:

        here_Identified_Notes2 = ' '.join(map(str,Identified_Notes2))
        here_Identified_Notes = ' '.join(map(str,Identified_Notes))

        if len(here_Identified_Notes2) or len(here_Identified_Notes) >= 0:
            mjaw = str("c''")
            f = open('myfile.ly', 'w')
            f.write('\\header{\n')
            f.write('title = ""\n')
            f.write('}\n')
            f.write('\\relative '+mjaw+' {\n')
            f.write(str(here_Identified_Notes2))
            f.write('\n}\n')
            f.write('\\chords {\n')
            f.write(str(here_Identified_Notes))
            f.write('\n}\n')
            f.write('\\addlyrics {\n')
            f.write('\n')
            f.write('}\n')
            f.write(
                '\\version "2.19.55" % necessary for upgrading to future LilyPond versions.')
            f.close()
            #clear our list after the save
            del mynotelist[:]
            os.system('open myfile.ly')
                    
        else:
                messagebox.showinfo(
                    "Play it first", "First you have to play the sound before saving.")
    else:
        messagebox.showinfo("Nothing to save",
                            "First open a file or record audio!")

def handWrite():
    import handwrite
def About():
    # Hide all the elements on the frame.
    openfileBtn.place_forget()
    frequencylbl.place_forget()
    input_audio_file.place_forget()
    SpinboxLbl.place_forget()
    Spinbox.place_forget()
    startBtn.place_forget()
    recordBtn.place_forget()
    # Show every element on the frame
    def show_everything():
        frequencylbl.place(x=300, y=230)
        input_audio_file.place(x=15, y=430)
        Spinbox.place(x=560, y=120)
        SpinboxLbl.place(x=425, y=120)
        startBtn.place(x=15, y=15)
        openfileBtn.place(x=220, y=15)
        recordBtn.place(x=425, y=15)

    def frameAbout():
        def hide_everything():
            returnBtn.place_forget()
            label_to_Watch.place_forget()
            # Draw everything on the main page
            show_everything()

        returnBtn = Button(root, text="GO BACK", fg="blue",command=hide_everything)
        returnBtn.place(x=10,y=10)

        label_to_Watch = Label(root, text="NIGGA CSHIGA")
        label_to_Watch.place(x=10,y=30)

    frameAbout()




menubar = Menu(root)
mymenu = Menu(root)
root.config(menu=mymenu)

submenu = Menu(mymenu)

mymenu.add_cascade(label="File", menu=submenu)

submenu.add_command(label="Remove audio", command=removeAudio)
submenu.add_command(label="Save file", command=save_file_to_lilypond)
submenu.add_command(label="Hand Write Notes", command=handWrite)
submenu.add_command(label="About", command=About)
submenu.add_command(label="Quit", command=quit)

# Main loop for the programm
root.geometry("640x480")
root.resizable(False, False)
root.title("Welcome")
root.mainloop()
