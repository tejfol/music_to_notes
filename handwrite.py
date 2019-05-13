from tkinter import *
import os

def create_save_window():
    mjaw = str("c''")
    f = open('HandWritedNotes.ly', 'w+')
    f.write('\\header{\n')
    f.write('title = #Here comes your Title\n')
    f.write('}\n')
    f.write('\\relative '+mjaw+' {\n')
    f.write('\\key g \\major\n')
    f.write('\\time 6/8\n')
    f.write('#Here comes your notes.')
    f.write('\n}\n')
    f.write('\\addlyrics {\n')
    f.write('#The lyrics \n')
    f.write('}\n')
    f.write(
        '\\version "2.19.55" % necessary for upgrading to future LilyPond versions.')
    f.close()

    os.system('open HandWritedNotes.ly')

create_save_window()