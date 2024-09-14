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

def sustain_note_indef(note=60, velocity=100):
    # Start playing the note
    synth.noteon(0, note, velocity)
    
    # Wait for a flag or event to stop the note
    while not stop_event.is_set():
        time.sleep(0.1)  # A small delay to avoid busy-waiting

    # Stop the note when the event is set
    synth.noteoff(0, note)

# Event flag to signal when to stop the note
stop_event = threading.Event()

# Start the thread to sustain the note
def check(fingers, i):
    stop_event = threading.Event()
    if i == 0:
        note_thread1 = threading.Thread(target=sustain_note_indef, args=(48,100))
        note_thread1.start()
    if i == 1:
        note_thread2 = threading.Thread(target=sustain_note_indef, args=(50,100))
        note_thread2.start()
    if i == 2:
        note_thread3 = threading.Thread(target=sustain_note_indef, args=(52,100))
        note_thread3.start()
    if i == 3: 
        note_thread4 = threading.Thread(target=sustain_note_indef, args=(54,100))
        note_thread.start()
    for f in fingers:
        for x in notes:
            if f != (x-48)//2:
                stop_event.set()
    note_thread1.join()
    note_thread2.join()
    note_thread3.join()
    note_thread4.join()

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


