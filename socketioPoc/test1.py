#!/usr/bin/env python3

from aiohttp import web
import socketio
import os

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    with open(os.path.join(current_file_dir, "index.html")) as f:
        return web.Response(text=f.read(), content_type='text/html')

async def socketiojs(request):
    with open(os.path.join(current_file_dir, "socket.io.js")) as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('message')
def print_message(sid, message):
    print("Socket ID: " , sid)
    print(message)

app.router.add_get('/', index)
app.router.add_get('/socket.io.js', socketiojs)

if __name__ == '__main__':
    web.run_app(app)