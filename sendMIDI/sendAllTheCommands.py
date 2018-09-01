#!/usr/bin/env python3

'''
We need to send the commands for the leds on the Novation keyboard on 
midi channel 16, so the first number is (binary): xxxx1111, so in hex
the number must end on an F. 

To toggle the led of the pad a NOTE_ON message must be sent, this is a 
9 according to the MIDI spec so the number becomes: 10011111, in hex:
9F. 

Pads in basic mode are notes C1 to B1 for the square pads (let's ignore
the round pads for now). These correspond to 0x24 to 0x33. In InControl
mode the notes are C6 to C8 and they include the round pads. 0x60 to 
0x78 in hex.

The second data byte of these messages determines the colour (velocity 
or controller value), to make the pad light up green use 64 (0x40)
'''

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midioutput

log = logging.getLogger('midiout')
logging.basicConfig(level=logging.DEBUG)

channel_voice_message=0x9F
colour_code=0x40 #0x40 is green
start_note_basic=0x24
start_note_inControl=0x60
midi_message=[channel_voice_message, start_note_basic, colour_code]

port=0 #should connect to Launchkey MIDI 2

try:
    midiout, port_name = open_midioutput(port=2,interactive=False,port_name="output")
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Sleeping for 10 seconds, make the connection please")
time.sleep(10)

for x in range(128):
    message=[channel_voice_message, x, colour_code]
    print(message)
    midiout.send_message(message)

del midiout
print("Exit.")