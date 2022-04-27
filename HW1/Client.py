from os import stat
import re
import socket
import threading

from Logger import Logger
from SocketMessage import SocketMessage

class State:
    waiting = "WAITING"
    playing = "PLAYING"

host = '127.0.0.1'
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
state = State.waiting


def read_from_server():
    while True:
        data = server.recv(1024).decode('ascii')
        data = SocketMessage.from_text(data)
        if (data.is_valid):
            process_message(data.message)
        if (data.message == 'server_disconnected'):
            Logger.log("Server disconnected, waiting for new game server")
            break


def process_message(message):
    print(message)


def start_game():
    state = State.playing
    reading_thread = threading.Thread(target=read_from_server)
    reading_thread.start()
    while True:
        command = input()
        process_command(command)


def process_command(command):
    if (state == State.waiting):
        print("Not connected to a server yet")
        return
    location = re.search("play (\d{1}) (\d{1})", command)
    if (location != None):
        x, y = location.group(1), location.group(2)
        data = SocketMessage.from_data("play_turn", {"x": x, "y": y})
        server.send(data.stringify())
    elif(command == "exit"):
        pass
    else:
        print("Invalid command")


server.connect((host, port))
Logger.log("Connected Successfully")

while True:
    data = server.recv(1024).decode('ascii')
    data = SocketMessage.from_text(data)
    Logger.log(f"Server: \n{data.message}")
    if (data.is_valid and data.message == 'server_connected'):
        Logger.log("Game started")
        start_game()

# check for game server disconnected
