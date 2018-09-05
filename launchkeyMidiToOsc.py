#!/usr/bin/env python3
#
# test_midiin_callback.py
#
"""Translates the MIDI messages from the Launchkey MIDI controler to OSC messages for Sonic Pi"""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import NOTE_ON
from rtmidi.midiconstants import CONTROL_CHANGE
from rtmidi.midiconstants import PITCH_BEND

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        self.build_osc_string(message)

    def build_osc_string(self,message):
        '''map the different sections of the midi keyboard to different addresses
            to make it easier to filter on them in Sonic Pi:
                - transport controls:   /transport/{rewind,fast_forward,stop,start,loop,record}
                - pitch wheel:          /pitch
                - modulation wheel:     /mod
                - sliders:              /slider/{1-9}
                - buttons:              /button/{1-9}
                - rotary controls:      /rotary/{1-8}
                - launch pads:          /pad/{A1-A8,B1-B8}
                - round buttons:        /button/{A,B}
                - keys:                 /note/{36-96}
        '''

        def message_to_filter(message):

            def get_midi_channel(message):
                '''The midi channel is the last nibble of the first byte of the midi message'''
                channel = (message[0] & 0x0F) + 1 #set the first nibble to all zeroes and add 1 (values 0-15 correspond to channel 1-16)
                print('Channel = ' + format(channel,'04b') + ': ' + str(channel)) #print 4 bits binary representation
                return channel

            def get_midi_command(message):
                '''The midi command is the first nibble of the first byte of the midi message'''

                def midi_command_to_string(command):
                    switcher = {
                        NOTE_ON: "note_on",
                        CONTROL_CHANGE: "control_change",
                        PITCH_BEND: "pitch_bend"
                    }
                    print(switcher.get(command, None))
                    return switcher.get(command, None)

                command = message[0] & 0xF0
                print('Command = ' + format(command,'04b') + ': ' + str(command))
                return midi_command_to_string(command)

            def note_on(message):
                if 36 <= message[1] <= 96 and get_midi_channel(message) != 10 :
                    return '/note/' + str(message[1])
                elif 36 <= message[1] <= 51 and get_midi_channel(message) == 10 :
                    return '/pad/'
                else:
                    return None

            def control_change(message):
                return 'not_implemted_yet'
            
            def pitch_bend(message):
                return 'not_implemted_yet'

            def command_to_filter_string(command):
                switcher = {
                    'note_on': note_on,
                    'control_change': control_change,
                    'pitch_bend': pitch_bend
                }
                #get function from switcher
                #func = switcher.get(command, lambda: "Invalid command")
                func = switcher.get(command, None)
                # Execute the function
                if func:
                    return func(message)
                else: 
                    return ''

            return command_to_filter_string(get_midi_command(message))


        
        print(message_to_filter(message))

    




    
    


# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port=1,client_name="MIDI logger",interactive=False,port_name="LaunchkeyIN")
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

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
    del midiin


