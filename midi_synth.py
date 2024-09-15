import tinysoundfont
import time
import threading

# Info for SoundFont florestan-subset.sfo
# 0 - 2 : Piano
# 0 - 10 : Music Box
# 0 - 12 : Marimba
# 0 - 19 : Church Org.1
# 0 - 21 : Accordion Fr
# 0 - 24 : Nylon-str.Gt
# 0 - 38 : Synth Bass 1
# 0 - 40 : Violin
# 0 - 45 : PizzicatoStr
# 0 - 55 : OrchestraHit
# 0 - 61 : Brass 1
# 0 - 75 : Pan Flute
# 0 - 87 : Bass & Lead
# 0 - 90 : Polysynth
# 0 - 97 : Soundtrack
# 0 - 109 : Bagpipe
# 0 - 116 : Taiko

synth = tinysoundfont.Synth()
sfid = synth.sfload("/Users/alxli/Documents/CS Projects/2024 HackMIT/florestan-subset.sfo")
synth.program_select(0, sfid, 0, 2) #select instrument type
synth.start()
notes = [48, 50, 52, 54]

def sustain_note_indef(note, velocity):
    # Start playing the note
    synth.noteon(0, note, velocity)
    
    # Wait for a flag or event to stop the note
    while flags[(note-48)//2] == True:
        time.sleep(0.1)  # A small delay to avoid busy-waiting

    # Stop the note when the event is set
    synth.noteoff(0, note)
    flags[(note-48)//2] = True

# Event flag to signal when to stop the note
# Start the thread to sustain the note
def check(fingers, i, flags, newFlags):
    if i == 0 and newFlags[i] == True:
        sustain_note_indef(48, 100)
        newFlags[i] = False
    if i == 1 and newFlags[i] == True:
        sustain_note_indef(50, 100)
        newFlags[i] = False
    if i == 2 and newFlags[i] == True:
        sustain_note_indef(52, 100)
        newFlags[i] = False
    if i == 3 and newFlags[i] == True: 
        sustain_note_indef(54, 100)
        newFlags[i] = False
    for f in fingers:
        for x in notes:
            if f != (x-48)//2: #if fingers aren't touching
                flags[f] = False
                newFlags[f] = True
            # else: #if fingers ARE touching
            #     newFlags[f] = True

                

# time.sleep(0.1)
# synth.noteoff(0, 52)
# time.sleep(0.1)
# synth.noteon(0, 51, 100)
# time.sleep(0.1)
# synth.noteoff(0, 51)
# time.sleep(0.1)
# synth.noteon(0, 50, 100)
# time.sleep(0.1)
# synth.noteoff(0, 50)
# time.sleep(1)


