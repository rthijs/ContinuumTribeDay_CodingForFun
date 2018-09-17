#!/usr/bin/env python3

'''launch this and connect with a browser to port 8080'''

import os

from aiohttp import web

current_file_dir = os.path.dirname(__file__)

def index(request):
    with open(os.path.join(current_file_dir, "index.html")) as f:
        return web.Response(text=f.read(), content_type='text/html')

def socketiojs(request):
    with open(os.path.join(current_file_dir, "socket.io.js")) as f:
        return web.Response(text=f.read())

def jqueryjs(request):
    with open(os.path.join(current_file_dir, "jquery-3.3.1.min.js")) as f:
        return web.Response(text=f.read())

def stylecss(request):
    with open(os.path.join(current_file_dir, "style.css")) as f:
        return web.Response(text=f.read())

app = web.Application()

app.router.add_get('/', index)
app.router.add_get('/socket.io.js', socketiojs)
app.router.add_get('/jquery-3.3.1.min.js', jqueryjs)
app.router.add_get('/style.css', stylecss)

web.run_app(app)
