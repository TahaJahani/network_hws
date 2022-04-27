from ast import arg
from pydoc import cli
import socket
import threading
from queue import Queue

from HashTable import HashTable
from Logger import Logger
from SocketMessage import SocketMessage

max_clients = 100
host = '127.0.0.1'
clients_port = 8000
servers_port = 3000

clients = []
waiting_clients = Queue()
free_game_servers = Queue()
# server_client_map = HashTable(50)


def read_from_client(client: socket.socket, server: socket.socket):
    try:
        while True:
            data = client.recv(1024)
            server.send(data)
    except:
        clients.remove(client)
        server.send(SocketMessage.from_message("Message", "user_disconnected"))
        free_game_servers.put(server)
        Logger.log(f"Client {client.getpeername()} disconnected")


def write_to_client(client: socket.socket, server: socket.socket):
    try:
        while True:
            data = server.recv(1024)
            client.send(data)
    except:
        waiting_clients.put(client)
        # TODO: send a message to client to tell him to wait
        Logger.log(f"Game server {server.getpeername()} disconnected")



def accept_clients():
    client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_server.bind((host, clients_port))
    client_server.listen(max_clients)
    Logger.log("Listening for clients to connect")
    while True:
        client, address = client_server.accept()
        Logger.log(f"Client {address} accepted")
        clients.append(client)
        waiting_clients.put(client)
        check_for_free_clients_or_servers()


def accept_game_servers():
    game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game_server.bind((host, servers_port))
    game_server.listen(max_clients)
    Logger.log("Listening for game servers to connect")
    while True:
        game_socket, address = game_server.accept()
        Logger.log(f"Game Server {address} accepted")
        free_game_servers.put(game_socket)
        check_for_free_clients_or_servers()


def check_for_free_clients_or_servers():
    if (waiting_clients.empty() or free_game_servers.empty()):
        return
    client = waiting_clients.get()
    game_server = free_game_servers.get()
    # server_client_map.set_val(game_server, client)
    # so we can get client from server and server from client
    # server_client_map.set_val(client, game_server)
    server_and_client_connected(client, game_server)


def server_and_client_connected(client: socket.socket, game_server: socket.socket):
    client.send(SocketMessage.from_message("Message", "server_connected").stringify())
    game_server.send(SocketMessage.from_message("Message", "user_connected").stringify()) #TODO: player can choose his type

    client_to_server_thread = threading.Thread(
        target=read_from_client, args=(client, game_server, ))
    server_to_client_thread = threading.Thread(
        target=write_to_client, args=(client, game_server, ))
    client_to_server_thread.start()
    server_to_client_thread.start()
    Logger.log(f"Client {client.getpeername()} connected to server {game_server.getpeername()}")


def get_input():
    # todo: get user input from console
    input_command = input()
    pass


client_accept_thread = threading.Thread(target=accept_clients)
game_server_accept_thread = threading.Thread(target=accept_game_servers)
web_server_thread = threading.Thread(target=get_input)

client_accept_thread.start()
game_server_accept_thread.start()
web_server_thread.start()
