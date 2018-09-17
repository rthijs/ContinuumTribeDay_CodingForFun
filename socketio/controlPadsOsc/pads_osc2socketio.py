#!/usr/bin/env python3

'''translates osc messages from sonic pi to socket io messages for the front end'''

import argparse
import asyncio
import socketio
from aiohttp import web
from pythonosc import dispatcher, osc_server

from socketIO_client import SocketIO

socketIO = SocketIO('localhost', 8081)

def pad_active_handler(address, data):
    print('in pad_active_handler: ' + data)
    socketIO.emit('pad_info_active', data)


def pad_enabled_handler(address, data):
    print('in pad_enabled_handler: ' + data)
    socketIO.emit('pad_info_enabled', data)


def pad_text_handler(address, data):
    print('in pad_text_handler: ' + data)
    socketIO.emit('pad_info_text', data)

dispatcher = dispatcher.Dispatcher()

dispatcher.map("/pad_active", pad_active_handler)
dispatcher.map("/pad_enabled", pad_enabled_handler)
dispatcher.map("/pad_text", pad_text_handler)

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
parser.add_argument("--port", type=int, default=5005,
                    help="The port to listen on")
args = parser.parse_args()

server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
