#!/usr/bin/env python3

'''Run this and go to localhost:8080'''

from aiohttp import web
import socketio
import os

import asyncio

from pythonosc import udp_client
from pythonosc import osc_message_builder

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

command = 'sample :bd_fat' #Sonic Pi code to execute, can be a large block of code, this is just a poc
UDP_IP = "127.0.0.1"
UDP_PORT = 4557 #4557 not 4559 for the SP gui, we need to talk to the server, not the gui
GUI_ID = 'SONIC_PI_PYTHON' #can be whatever but it's mandatory
RUN_COMMAND = "/run-code"

client = udp_client.UDPClient(UDP_IP,UDP_PORT)

async def index(request):
    with open(os.path.join(current_file_dir, "index.html")) as f:
        return web.Response(text=f.read(), content_type='text/html')

async def socketiojs(request):
    with open(os.path.join(current_file_dir, "socket.io.js")) as f:
        return web.Response(text=f.read())

async def jqueryjs(request):
    with open(os.path.join(current_file_dir, "jquery-3.3.1.min.js")) as f:
        return web.Response(text=f.read())

@sio.on('pad_hit')
async def handle_pad_hit(sid, message):
    print("pad hit: ", message)
    command = 'sample :bd_fat' #Sonic Pi code to execute
    msg = osc_message_builder.OscMessageBuilder(address=RUN_COMMAND)
    msg.add_arg('SONIC_PI_PYTHON')
    msg.add_arg(command)
    msg = msg.build()
    client.send(msg)
    #await sio.emit("broadcast", {'key':'value'})
    asyncio.ensure_future(sio.emit("broadcast", {'key':'value'}))


app.router.add_get('/', index)
app.router.add_get('/socket.io.js', socketiojs)
app.router.add_get('/jquery-3.3.1.min.js', jqueryjs)

if __name__ == '__main__':
    web.run_app(app)