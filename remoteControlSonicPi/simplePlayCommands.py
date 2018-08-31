#!/usr/bin/env python3

'''It is possible to remotely control Sonic Py by sending OSC commands

find the discussion here: https://groups.google.com/forum/#!topic/sonic-pi/7vDgNhQXfmo

tldr: you have to send two arguments with the /run-code path: the first is a "gui id", and the second is the command as a string, i.e. "play 60".

working implementation copied from: https://github.com/gkvoelkl/python-sonic/blob/master/psonic/synth_server.py
'''

from pythonosc import udp_client
from pythonosc import osc_message_builder

command = 'play 60' #Sonic Pi code to execute, can be a large block of code, this is just a poc

UDP_IP = "127.0.0.1"
UDP_PORT = 4557 #4557 not 4559 for the SP gui, we need to talk to the server, not the gui
GUI_ID = 'SONIC_PI_PYTHON' #can be whatever but it's mandatory

RUN_COMMAND = "/run-code"

client = udp_client.UDPClient(UDP_IP,UDP_PORT)
msg = osc_message_builder.OscMessageBuilder(address=RUN_COMMAND)
msg.add_arg('SONIC_PI_PYTHON')
msg.add_arg(command)
msg = msg.build()
client.send(msg)