#!/usr/bin/env python3

#
"""Show how to open an output port and send MIDI events."""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midioutput


log = logging.getLogger('midiout')
logging.basicConfig(level=logging.DEBUG)

port=0 #should connect to Launchkey MIDI 2

try:
    midiout, port_name = open_midioutput(port=2,interactive=False,port_name="output")
except (EOFError, KeyboardInterrupt):
    sys.exit()

extended_mode_online_message = [159, 12, 127]  # When the keyboard enters Extended mode the InControl buttons should light up
test_message = [159, 36, 56]

print("Sleeping for 5 seconds, make the connection please")
time.sleep(5)
print("Sending test message")
midiout.send_message(test_message)

del midiout
print("Exit.")