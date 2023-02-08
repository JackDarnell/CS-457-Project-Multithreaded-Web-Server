#lab code, need to modify to work for the project
import socket

server_ip = 'localhost'
server_port = 12000
buffer_size = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

connection_socket, addr = server_socket.accept()

msg1 = connection_socket.recv(buffer_size).decode('ascii')
msg2 = connection_socket.recv(buffer_size).decode('ascii')
print('first message: ', msg1)
print('second message: ', msg2)

connection_socket.close()
server_socket.close()