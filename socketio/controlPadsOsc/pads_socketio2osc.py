#!/usr/bin/env python3

'''translates socket io messages from the gui to osc messages for sonic pi'''

import socketio
from aiohttp import web
from pythonosc import udp_client

sio = socketio.AsyncServer()
sio.__setattr__('origins', '*:*')  # prevent Cross-Origin Request Blocked error
app = web.Application()
sio.attach(app)

SP_IP = "127.0.0.1"
SP_PORT = 4559  # Sonic Pi GUI
osc_client = udp_client.SimpleUDPClient(SP_IP, SP_PORT)


@sio.on('connect')
async def connect(sid, environ):
    print("connect ", sid)


@sio.on('pad_hit')
async def handle_pad_hit(sid, data):
    print("pad_hit ", data)
    osc_client.send_message('pad', data)

@sio.on('pad_info_text')
async def handle_pad_info_text(sid, data):
    print('pad info text: ' + data )

@sio.on('pad_info_active')
async def handle_pad_info_active(sid, data):
    print('pad info active: ' + data )

@sio.on('pad_info_enabled')
async def handle_pad_info_enabled(sid, data):
    print('pad info enabled: ' + data )


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


web.run_app(app, port=8081)
