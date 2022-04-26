import socket
import threading

from Logger import Logger

host = '127.0.0.1'
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))
Logger.log("Connected Successfully")
data = server.recv(1024)
Logger.log(data)
# Should wait until a confirm message from WebServer is received. then we create two threads for read and write