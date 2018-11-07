#!/usr/bin/env python3

"""Listen for midi note_on / note_off messages and map them to different notes"""

import sys
import time

from rtmidi.midiutil import open_midiinput, open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON


class MidiInputHandler(object):

    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):

        def change_note(note):
            tonica = 60 # do
            kwint = 67 # sol
            kwart = 65 # fa
            sext = 69 # la
            terts = 64 # mi

            '''
            new order of keys on the keyboard: 
               ... A F C-8 *C* C+8 G E A F C C+8 C+16 G + 8 ...
            '''
            if note in [60,69,50]:
                return tonica
            
            if note in [62,71]:
                return tonica + 12 # octave higher

            if note in [59,48]:
                return tonica - 12 # octave lower

            if note == 72:
                return tonica + 24 # + 2 octaves

            if note in [64,52]:
                return kwint

            if note in [69,57]:
                return kwart

            if note in [67,55]:
                return sext
            
            if note in [65,53]:
                return terts
        
        def play_midi(message):
            print(message)
            if (message[0] == NOTE_ON or message[0] == NOTE_OFF):
                note = change_note(message[1])
                velocity = message[2]
                new_message = [message[0], note, velocity]
                midiout.send_message(new_message)
            print ('playing midi')

        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        play_midi(message)






# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, in_port_name = open_midiinput(port=1,client_name="MIDI mapper",interactive=False,port_name="MidiMapper_input")
    midiout, out_port_name = open_midioutput(port=1,client_name="MIDI mapper",interactive=False,port_name="MidiMapper_output")
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(in_port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    midiout.close_port()
    del midiin
    del midiout