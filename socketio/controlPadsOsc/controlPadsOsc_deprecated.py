#!/usr/bin/env python3

'''Run this and go to localhost:8080'''

from aiohttp import web
import socketio
import os
import asyncio
import argparse
import multiprocessing

from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import dispatcher

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

UDP_IP = "127.0.0.1"
UDP_PORT = 4559 #Sonic Pi GUI

client = udp_client.SimpleUDPClient(UDP_IP,UDP_PORT)

dispatcher = dispatcher.Dispatcher()

async def index(request):
    with open(os.path.join(current_file_dir, "index.html")) as f:
        return web.Response(text=f.read(), content_type='text/html')

async def socketiojs(request):
    with open(os.path.join(current_file_dir, "socket.io.js")) as f:
        return web.Response(text=f.read())

async def jqueryjs(request):
    with open(os.path.join(current_file_dir, "jquery-3.3.1.min.js")) as f:
        return web.Response(text=f.read())

async def stylecss(request):
    with open(os.path.join(current_file_dir, "style.css")) as f:
        return web.Response(text=f.read())

@sio.on('pad_hit')
async def handle_pad_hit(sid, message):
    print("pad hit: ", message)
    client.send_message('pad', message)
    await broadcast_message('broadcast', {'key':'value'})

async def broadcast_message(address, data):
    asyncio.ensure_future(sio.emit(address, data))

async def sonic_pi_test_handler(address, data):
    #await sio.emit("broadcast", {'key':'value'})
    #asyncio.ensure_future(sio.emit("broadcast", {'key':'value'}))
    #sio.emit("broadcast", {'key':'value'})
    print('in sonic_pi_test_handler')
    #asyncio.ensure_future(sio.emit("broadcast", {'key':'value'}))
    #await broadcast_message('broadcast', {'key':'value'})

def pad_active_handler(address, data):
    print('in pad_active_handler')
    sio.emit('pad_active', {'0':'0'})

def pad_enabled_handler(address, data):
    print('in pad_enabled_handler')
    sio.emit('pad_enabled', {'0':'0'})

def pad_text_handler(address, data):
    print('in pad_text_handler')
    sio.emit('pad_text', {'0':'PAD 0'})

async def web_server_local():
    web.run_app(app)

async def osc_server_local():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher.map("/sonicpitest**", sonic_pi_test_handler)
    dispatcher.map("/pad_active", pad_active_handler)
    dispatcher.map("/pad_enabled", pad_enabled_handler)
    dispatcher.map("/pad_text", pad_text_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

async def main():
    asyncio.ensure_future(web_server_local())
    asyncio.ensure_future(osc_server_local())

app.router.add_get('/', index)
app.router.add_get('/socket.io.js', socketiojs)
app.router.add_get('/jquery-3.3.1.min.js', jqueryjs)
app.router.add_get('/style.css', stylecss)

loop = asyncio.get_event_loop() 
loop.run_until_complete(main())

#p1 = multiprocessing.Process(name='web_server', target=web_server_local)
#p2 = multiprocessing.Process(name='osc_server', target=osc_server_local)

#p1.start()
#p2.start()