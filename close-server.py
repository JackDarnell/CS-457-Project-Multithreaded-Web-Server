#lab code, need to modify to work for the project
import socket, os

server_ip = 'localhost'
server_port = 80
buffer_size = 1000024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.close()