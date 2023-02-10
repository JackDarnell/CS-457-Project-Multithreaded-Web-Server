#lab code, need to modify to work for the project
import socket, os

server_ip = 'localhost'
server_port = 1699
buffer_size = 1000024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

def sendMessage(responseLines, content):
    connection_socket.send(responseLines.encode('ascii'))
    connection_socket.send(content)
    #connection_socket.send("\r\n\r\n".encode('ascii'))
    connection_socket.close()

def send404():
    print("\nfile not found, responding with a 404\n")
    responseLines = "HTTP/1.1 404 Not Found\r\n"
    responseLines += "Connection: close\r\n"
    responseLines += "Content-Type: text/html\r\n\r\n"
    content = open("./content/404.html", 'rb').read()
    sendMessage(responseLines, content)

while True:
    print("\nloop start\n")
    connection_socket, addr = server_socket.accept()

    msg1 = connection_socket.recv(buffer_size).decode('ascii')

    request = msg1.partition('\n')[0]
    fileRequested = request.split(' ')[1]

    if fileRequested == "/":
        fileRequested = "/greeting.html"

    fileRequested = fileRequested.split('/', 1)[1]

    #if the file requested is the stop command, break out of the loop
    testStop = fileRequested[-4:]
    if(testStop == "stop"):
        print("\nstop command received, breaking out of loop\n")
        break

    fileRequested = "./content/"+fileRequested

    contentType="error"

    try:
        contentType = fileRequested.split('.')[2]
    except:
        print("\nno content type found\n")

    print("\ncontent type: " + contentType)

    if(contentType == "html"):
        contentType = "text/html"
    elif(contentType == "jpeg"):
        contentType = "image/jpeg"
    elif(contentType == "jpg"):
        contentType = "image/jpeg"
    elif(contentType == "png"):
        contentType = "image/png"
    elif(contentType == "txt"):
        contentType = "text/plain"


    print("file requested: " + fileRequested)

    if(os.path.isfile(fileRequested) and contentType != "error"):
        print("\nfile found\n")
        responseLines = "HTTP/1.1 200 OK\r\n"
        responseLines += "Connection: close\r\n"
        responseLines += "Content-Type: " + contentType + "\r\n\r\n"
        content = open(fileRequested, 'rb').read()
        sendMessage(responseLines, content)
    else:
        send404()

print("\nServer no longer running\n")
responseLines = "HTTP/1.1 200 OK\r\n"
responseLines += "Connection: close\r\n"
responseLines += "Content-Type: text/html" + "\r\n\r\n"
content = open("./content/serverDoneRunning.html", 'rb').read()
sendMessage(responseLines, content)
server_socket.close()