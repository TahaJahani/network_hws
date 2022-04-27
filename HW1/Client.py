from ast import arg
import os
import re
import socket
import threading

from Logger import Logger
from SocketMessage import SocketMessage


class State:
    waiting = "WAITING"
    playing = "PLAYING"
    finished = "FINISHED"


host = '127.0.0.1'
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
state = State.waiting


def read_from_server():
    global state
    while True:
        data = server.recv(1024).decode('ascii')
        if (data == b''):
            break
        data = SocketMessage.from_text(data)
        if (data.is_valid):
            print(data.message)
        if (data.message == 'server_disconnected'):
            state = State.waiting
            Logger.log("Server disconnected, waiting for new game server")
            break
        if data.message.endswith('won the game!'):
            state = State.finished
            server.close()
            break


def start_game():
    global state
    state = State.playing
    read_from_server()


def get_input():
    while True:
        command = input()
        process_command(command)


def process_command(command):
    global state
    if (state == State.waiting):
        print("Not connected to a server yet")
        return
    location = re.search("/play (\d{1}) (\d{1})", command)
    if (location != None):
        x, y = location.group(1), location.group(2)
        data = SocketMessage.from_data("play_turn", {"x": x, "y": y})
        server.send(data.stringify())
    elif(command == "/exit"):
        server.sendall(SocketMessage.from_message("Message", "exit").stringify())
        server.close()
        state = State.finished
        os._exit(0)
    else:
        print("Invalid command")


server.connect((host, port))
Logger.log("Connected Successfully")

get_input_thread = threading.Thread(target=get_input)
get_input_thread.setDaemon(True)
get_input_thread.start()

while True:
    data = server.recv(1024).decode('ascii')
    data = SocketMessage.from_text(data)
    Logger.log(f"Server: \n{data.message}")
    if (data.is_valid and data.message == 'server_connected'):
        Logger.log("Game started")
        start_game()
