#!/usr/bin/env python3

#python-osc only works with python 3 so make sure to set your environment!

#official python-osc website: https://pypi.org/project/python-osc/
#code taken from the example code there

"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=4559, #4559 is the port where Sonic Pi listens
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  for x in range(10):
    client.send_message("/filter", random.random())
    time.sleep(1)