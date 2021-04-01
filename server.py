import asyncio
import websockets
import json
import os
import socket
import ssl
from game import *


PORT = 443
IP = socket.gethostbyname(socket.gethostname())
NUMOFPLAYERS = 2

games = set() #collection of all games
games.add(Game())

async def addToGame(game, player):
    game.players.append(player)
    await game.sendAll({"action": "playerJoined", "players": len(game.players), "max": NUMOFPLAYERS})

async def regester(websocket, path):
    print(f"{websocket.remote_address} connected")
    player = Player(websocket)
    bool = True
    for game in games:  #adds player to game if there is room
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

#open certificate
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile= os.path.join(".\\TLS", "cert.pem"), keyfile= os.path.join(".\\TLS", "key.pem"))

#starts server
start_server = websockets.serve(regester, IP, PORT, ssl = ssl_context)
print(f"Starting Server on {IP}:{PORT}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
