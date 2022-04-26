import socket
import threading

from Logger import Logger


class Status:
    WAITING = 1
    PLAYING = 2
    FINISHED = 3

class State:
    status = Status.WAITING
    board = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"],
    ]
    player = "O"

    def __init__(self, player):
        self.player = player


host = '127.0.0.1'
port = 3000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))
Logger.log("Connected Successfully")

state = None

def start_game(player):
    state = State(player)
    pass

def client_played(x, y):
    pass

def is_game_finished():
    pass
