from calendar import day_abbr
import socket
import threading
from queue import Queue
from time import sleep

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
            if (data == b''):
                handle_client_disconnected(client, server)
                break
            sleep(0.1)
            server.send(data)
    except:
        handle_game_server_disconnected(client, server)


def write_to_client(client: socket.socket, server: socket.socket):
    try:
        while True:
            data = server.recv(1024)
            if (data == b''):
                handle_game_server_disconnected(client, server)
                break
            sleep(0.1)
            client.send(data)
            data = SocketMessage.from_text(data)
            if (data.is_valid and data.message.endswith('won the game!')):
                handle_game_finished(client, server)
                break
    except:
        handle_client_disconnected(client, server)


def handle_game_finished(client: socket.socket, server: socket.socket):
    if (client in clients):
        clients.remove(client)
    free_game_servers.put(server)
    Logger.log(f"Game in server {server.getpeername()} finished")
    check_for_free_clients_or_servers()


def handle_game_server_disconnected(client: socket.socket, server: socket.socket):
    try:
        client.send(SocketMessage.from_message(
            "Message", "server_disconnected").stringify())
        waiting_clients.put(client)
    except:
        pass
    Logger.log(f"Game server {server.getsockname()} disconnected")


def handle_client_disconnected(client: socket.socket, server: socket.socket):
    if (client in clients):
        clients.remove(client)
    try:
        server.send(SocketMessage.from_message(
            "Message", "user_disconnected").stringify())
        free_game_servers.put(server)
    except:
        pass
    Logger.log(f"Client {client.getsockname()} disconnected")
    check_for_free_clients_or_servers()


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
    Logger.log("Trying to match a server to client...")
    # server_client_map.set_val(game_server, client)
    # so we can get client from server and server from client
    # server_client_map.set_val(client, game_server)
    server_and_client_connected(client, game_server)


def server_and_client_connected(client: socket.socket, game_server: socket.socket):
    try:
        Logger.log(
            f"Client {client.getpeername()} connected to server {game_server.getpeername()}")
    except:
        pass

    client.send(SocketMessage.from_message(
        "Message", "server_connected").stringify())
    game_server.send(SocketMessage.from_message(
        "Message", "user_connected").stringify())  # TODO: player can choose his type

    client_to_server_thread = threading.Thread(
        target=read_from_client, args=(client, game_server, ))
    server_to_client_thread = threading.Thread(
        target=write_to_client, args=(client, game_server, ))
    client_to_server_thread.start()
    server_to_client_thread.start()


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
