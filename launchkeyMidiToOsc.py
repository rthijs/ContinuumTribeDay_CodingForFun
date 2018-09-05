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

from pythonosc import udp_client

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

osc_ip = '127.0.0.1'
osc_port = 4559 #Sonic Pi
osc_client = udp_client.SimpleUDPClient(osc_ip,osc_port)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        osc_string = self.build_osc_string(message)
        if osc_string:
            osc_client.send_message(osc_string, [message[1], message[2]]) #note, velocity

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
                - round buttons:        /button/{A9,B9}
                - keys:                 /note
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
                    return '/note'
                elif 36 <= message[1] <= 51 and get_midi_channel(message) == 10 :
                    row = 'X'
                    column = 'Y'
                    rowA = [40,41,42,43,48,49,50,51]
                    rowB = [36,37,38,39,44,45,46,47]
                    if message[1] in rowA:
                        row = 'A'
                        column = rowA.index(message[1])
                    elif message[1] in rowB:
                        row = 'B'
                        column = rowB.index(message[1])
                    else:
                        print('This should never happen')
                        return None

                    return '/pad/' + row + str(column)
                else:
                    return None

            def control_change(message):

                transport = [112,113,114,115,116,117]
                mod = [1]
                slider = [41,42,43,44,45,46,47,48,7]
                button = [51,52,53,54,55,56,57,58,59]
                rotary = [21,22,23,24,25,26,27,28]
                round_pad = [104,105]

                if message[1] in transport:
                    transport_buttons = ['rewind','fast_forward','stop','start','loop','record']
                    return '/transport/' + transport_buttons[transport.index(message[1])]
                elif message[1] in mod:
                    return '/mod'
                elif message[1] in slider:
                    return '/slider/' + str(slider.index(message[1]))
                elif message[1] in button:
                    return '/button/' + str(button.index(message[1]))
                elif message[1] in rotary:
                    return '/rotary/' + str(rotary.index(message[1]))
                elif message[1] in round_pad:
                    pad_rows = ['A','B']
                    return '/button/' + pad_rows[round_pad.index(message[1])] + '9'
                else:
                    return None
            
            def pitch_bend(message):
                return '/pitch'

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
        return message_to_filter(message)

    
        

    






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


