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
import time



# showing the window
root = Tk()
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
name = ["C", "C'", "D", "D'", "E", "E'" "F", "F'", "G", "G'", "A", "A'", "B", "B'"]


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
    return name[n] #+ str(octave)

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


def create_save_window():
    if len(mynotelist) > 0:
        s_window = Toplevel(root)
        s_window.geometry("320x320")

        # Lyrics label
        lyricsLbl = Label(s_window, text="Lyrics:")
        lyricsLbl.place(x=6, y=150)

        # Entry lyrics
        entryForLyrics = Entry(s_window, width="15")
        entryForLyrics.place(x=58, y=148)

        # Title label
        entryLbl = Label(s_window, text="Title:")
        entryLbl.place(x=15, y=120)
        # Entry for the title of the header
        entryForTitle = Entry(s_window, width="15")
        entryForTitle.place(x=58, y=120)

        def save_to_pdf():
            here_mynotelist = ' '.join(map(str,mynotelist))
            

            if len(here_mynotelist) > 0:
                #Title for the file
                Title = entryForTitle.get()
                #Lyrics for the file
                Lyrics = entryForLyrics.get()
                #open the file and write the following lines
                mjaw = str("c''")
                f = open('myfile.ly', 'w')
                f.write('\\header{\n')
                f.write('title = "' + Title + '"\n')
                f.write('}\n')
                f.write('\\relative '+mjaw+' {\n')
                f.write('\\key g \\major\n')
                f.write('\\time 6/8\n')
                f.write(str(here_mynotelist))
                f.write('\n}\n')
                f.write('\\addlyrics {\n')
                f.write(str(Lyrics)+'\n')
                f.write('}\n')
                f.write(
                    '\\version "2.19.55" % necessary for upgrading to future LilyPond versions.')
                f.close()
                #clear our list after the save
                del mynotelist[:]
                os.system('open myfile.ly')
                s_window.destroy()
            else:
                messagebox.showinfo(
                    "Play it first", "First you have to play the sound before saving.")

         # Button to save
        saveSongBtn = Button(s_window, text="Save",
                             command=save_to_pdf, width="10")
        saveSongBtn.place(x=100, y=250)

    else:
        messagebox.showinfo("Nothing to save",
                            "First open a file or record audio!")

def handWrite():
    import handwrite

menubar = Menu(root)
mymenu = Menu(root)
root.config(menu=mymenu)

submenu = Menu(mymenu)

mymenu.add_cascade(label="File", menu=submenu)

submenu.add_command(label="Remove audio", command=removeAudio)
submenu.add_command(label="Save file", command=create_save_window)
submenu.add_command(label="Hand Write Notes", command=handWrite)
submenu.add_command(label="Quit", command=quit)

# Main loop for the programm
root.geometry("640x480")
root.title("Welcome")
root.mainloop()
