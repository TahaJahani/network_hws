import socket
import threading

from HashTable import HashTable
from Logger import Logger

max_clients = 100
host = '127.0.0.1'
clients_port = 8000
servers_port = 3000

clients = []
waiting_clients = []
free_game_servers = []
server_client_map = HashTable(50)

def handle_client():
    pass


def accept_clients():
    client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_server.bind((host, clients_port))
    client_server.listen(max_clients)
    Logger.log("Listening for clients to connect")
    while True:
        client, address = client_server.accept()
        Logger.log(f"Client {address} accepted")
        clients.append(client)


def accept_game_servers():
    game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game_server.bind((host, servers_port))
    game_server.listen(max_clients)
    Logger.log("Listening for game servers to connect")
    while True:
        game_server, address = game_server.accept()
        Logger.log(f"Game Server {address} accepted")


def connect_clients_to_servers():
    # todo: check for waiting clients and free servers
    pass


accept_clients()