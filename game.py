import random
import asyncio
import websockets
import json

class Card(object):
    #name: 2, 3, 4...J, Q, K, A
    #suit: diamonds, hearts, clubs, spades
    #color: red, black
    #Face Card: J, Q, K, A
    #value: 2 = 2, 3 = 3, ..., J = 10, Q = 10, K = 0, A = 1
    #flipped: True, False
    suitsList = ["spades", "hearts", "diamonds", "clubs"]
    namesList = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, name, suit):
        self.isFlipped = False
        self.name = name
        self.suit = suit

        if suit == "clubs" or suit == "spades":
            self.color = "black"
        else:
            self.color = "red"

        try:
            self.value = int(name)
        except ValueError:
            self.isFaceCard = True
            if name == "J" or name == "Q":
                self.value = 10
            elif name == "K":
                self.value = 0
            elif name == "A":
                self.value = 1
        else:
            self.isFaceCard = False

    def flip(self):
        if self.isFlipped:
            print("Card == already flipped")
            raise ValueError
        self.isFlipped = True

    def toHTML(self):
        num = 0
        if self.suit == "spades":
            num =  127137 + Card.namesList.index(self.name) + int(Card.namesList.index(self.name) > Card.namesList.index("J"))
        elif self.suit == "hearts":
            num =  127153 + Card.namesList.index(self.name) + int(Card.namesList.index(self.name) > Card.namesList.index("J"))
        elif self.suit == "diamonds":
            num =  127169 + Card.namesList.index(self.name) + int(Card.namesList.index(self.name) > Card.namesList.index("J"))
        elif self.suit == "clubs":
            num =  127185 + Card.namesList.index(self.name) + int(Card.namesList.index(self.name) > Card.namesList.index("J"))
        return "&#" + str(num) + ";"

    def toString(self):
        return "<name: " + self.name + ",\t" + "suit: " + self.suit + "flipped:" + self.isFlipped + ">"


class Deck:

    def __init__(self):
        self.cardList = []
        for suit in Card.suitsList:
            for name in Card.namesList:
                self.cardList.append(Card(name, suit))

    def shuffle(self):
        random.shuffle(self.cardList)

class Game:

    def __init__(self):
        self.deck = Deck()
        self.players = []

    async def start(self):
        print(" a game has started")
        self.deck.shuffle()
        for player in self.players:
            player.cards = self.deck.cardList[:4]
            del self.deck.cardList[:4]

        done, pending = await asyncio.wait([player.sendData({"action": "give", "cards": [card.toHTML() for card in player.cards]}) for player in self.players])
        for task in pending:
            task.cancel()
        await self.sendAll({"action": "start"})


    async def sendAll(self, data):
            await asyncio.wait([player.sendData(data) for player in self.players])


    def turn(self, player, turnNumber):

        sum = 0
        for card in player.cards:
            if card.isFlipped:
                sum += 1
        if sum == 4:
            return
        del sum




class Player:

    def __init__(self, socket):
        self.cards = []
        self.socket = socket
        self.isTurn = False


    async def sendData(self, data):
        print(json.dumps(data))
        await self.socket.send(json.dumps(data))
