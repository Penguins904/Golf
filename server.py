import asyncio
import websockets
import json
from game import *
from http import HTTPStatus
import functools
import os


PORT = 8080
IP = "192.168.86.50"
NUMOFPLAYERS = 2

games = set()
games.add(Game())



MIME_TYPES = {
    "html": "text/html",
    "js": "text/javascript",
    "css": "text/css"
}

async def process_request(sever_root, path, request_headers):
    """Serves a file when doing a GET request with a valid path."""

    if "Upgrade" in request_headers:
        return  # Probably a WebSocket connection

    if path == '/' or path == "":
        path = '/index.html'

    response_headers = [
        ('Server', 'asyncio websocket server'),
        ('Connection', 'close'),
    ]

    # Derive full system path
    full_path = os.path.realpath(os.path.join(sever_root, path[1:]))

    # Validate the path
    if os.path.commonpath((sever_root, full_path)) != sever_root or \
            not os.path.exists(full_path) or not os.path.isfile(full_path):
        print("HTTP GET {} 404 NOT FOUND".format(path))
        return HTTPStatus.NOT_FOUND, [], b'404 NOT FOUND'

    # Guess file content type
    extension = full_path.split(".")[-1]
    mime_type = MIME_TYPES.get(extension, "application/octet-stream")
    response_headers.append(('Content-Type', mime_type))

    # Read the whole file into memory and send it out
    body = open(full_path, 'rb').read()
    response_headers.append(('Content-Length', str(len(body))))
    print("HTTP GET {} 200 OK".format(path))
    return HTTPStatus.OK, response_headers, body



async def addToGame(game, player):
    game.players.append(player)
    await game.sendAll({"action": "playerJoined", "players": len(game.players), "max": NUMOFPLAYERS})

async def regester(websocket, path):
    print(f"{websocket.remote_address} connected")
    player = Player(websocket)
    bool = True
    for game in games:
        if len(game.players) < NUMOFPLAYERS:
            bool = False
            await addToGame(game, player)
            print(len(game.players))
            if len(game.players) is NUMOFPLAYERS:
                await game.start()
                break
    if bool:
        game = Game()
        await addToGame(game, player)


handler = functools.partial(process_request, os.getcwd())
start_server = websockets.serve(regester, IP, PORT,
                                    process_request=handler)
print(f"Starting Server on {IP}:{PORT}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
