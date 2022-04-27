from email import message
from os import stat
import random
import socket
import threading

from matplotlib.pyplot import text

from Logger import Logger
from SocketMessage import SocketMessage


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
    computer = "X"
    winner = None

    def __init__(self, player):
        self.player = player
        self.computer = "X" if player == "O" else "O"

    def get_filled_cells_count(self):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != '_':
                    count += 1
        return count


host = '127.0.0.1'
port = 3000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
state = State("O")


def get_command():
    while True:
        data = server.recv(1024).decode('ascii')
        Logger.log(f"Message received: {data}")
        data = SocketMessage.from_text(data)
        if (not data.is_valid):
            handle_invalid_request(data)
            continue
        if (data.message == 'user_disconnected'):
            handle_user_disconnected(data)
        elif (data.message == 'user_connected'):
            handle_user_connected(data)
        elif(data.message == 'play_turn'):
            handle_play_turn(data)


def handle_user_disconnected(socket_message):
    global state
    state = State("O")
    Logger.log("User exited the game, waiting for new user to connect")
    return


def handle_invalid_request(socket_message):
    resp = SocketMessage.from_message("Error", "Invalid request")
    server.send(resp.stringify())


def handle_user_connected(socket_message: SocketMessage):
    if (state.status != Status.WAITING):
        resp = SocketMessage.from_message(
            "Error", "Already connected to a user")
        server.send(resp.stringify())
        return
    player = "X"
    if ("player" in socket_message.data):
        player = socket_message.data['player']
    type, message = start_game(player)
    resp = SocketMessage.from_message(type, message)
    server.send(resp.stringify())
    Logger.log("User connected")


def handle_play_turn(socket_message: SocketMessage):
    pass


def start_game(player):
    global state
    state = State(player)
    state.status = Status.PLAYING
    if (player == 'O'):
        play_computer()
    return "Message", get_board()


def play_client(x, y):
    if (x > 3 or x < 1 or y > 3 or y < 1):
        return "Error", "Invalid x or y provided"
    x = x - 1
    y = y - 1
    if (state.board[x][y] != "_"):
        return "Error", "Cell is not empty"
    state.board[x][y] = state.player
    if (is_game_finished()):
        state.status = Status.FINISHED
        return "Message", f"{state.winner} won the game!"
        # TODO: send a message to server to be added to free list
    play_computer()
    if (is_game_finished()):
        state.status = Status.FINISHED
        return "Message", f"{state.winner} won the game!\n{get_board()}"
        # TODO: send a message to server to be added to free list
    return "Message", get_board()


def is_game_finished():
    for i in range(3):
        if (state.board[i][0] == state.board[i][1] and state.board[i][0] == state.board[i][2] and state.board[i][0] != '_'):
            state.winner = "Computer" if state.board[i][0] == state.computer else "You"
            return True
    for j in range(3):
        if (state.board[0][j] == state.board[1][j] and state.board[0][j] == state.board[2][j] and state.board[0][j] != '_'):
            state.winner = "Computer" if state.board[0][j] == state.computer else "You"
            return True
    if (state.board[1][1] != '_'):
        if ((state.board[0][0] == state.board[1][1] and state.board[0][0] == state.board[2][2]) or
                (state.board[0][2] == state.board[1][1] and state.board[0][0] == state.board[2][0])):
            state.winner = "Computer" if state.board[1][1] == state.computer else "You"
            return True
    if (state.get_filled_cells_count() == 9):
        state.winner = "Nobody"
        return True
    return False


def get_board():
    board = ''
    for i in range(3):
        board += f"{state.board[0][i]}|{state.board[1][i]}|{state.board[2][i]}\n"
    return board


def play_computer():
    random_x = random.randint(0, 3)
    random_y = random.randint(0, 3)
    while state.board[random_x][random_y] != '_':
        random_x = random.randint(0, 3)
        random_y = random.randint(0, 3)
    state.board[random_x][random_y] = state.computer


server.connect((host, port))
Logger.log("Connected Successfully")
Logger.log("Waiting for a user")
get_command()
