import socket
import threading

from Logger import Logger

host = '127.0.0.1'
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))
Logger.log("Connected Successfully")