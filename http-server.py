#lab code, need to modify to work for the project
import socket, os

server_ip = 'localhost'
server_port = 80
buffer_size = 1000024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

connection_socket, addr = server_socket.accept()


msg1 = connection_socket.recv(buffer_size).decode('ascii')

request = msg1.partition('\n')[0]
fileRequested = request.split(' ')[1]
fileRequested = fileRequested.split('/')[-1]

dir_path = os.path.dirname(os.path.realpath(__file__))

newFile = None
fileFound = False
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file == fileRequested:
            print("FIle Found: " + file + " dir path: " + dir_path + " root: " + root)
            print("\nthis is what i think " + root + "/" + file)
            fileFound = True
            newFile = open((root + "/" + file), 'w')

print(newFile)
if fileFound:
    #form message, would prob work better as a function but whatever
    statusLine = "HTTP/1.1 200 OK\r\n\r\n"
    body = newFile
    message = statusLine + body
    #msg = "HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\n" + "Content-Length: " + str(os.path.getsize(fileRequested)) + open(fileRequested) + "\r\n\r\n"
    connection_socket.send(message.encode('ascii'))
else:
    connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode('ascii'))


connection_socket.close()
server_socket.close()