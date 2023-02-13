
#written by: Jack Darnell
import socket, os, threading


server_ip = 'localhost'
server_port = 1699
buffer_size = 1000024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()
shouldStop = [False]

#new thread for each connection
def clientThread(connection_socket, shouldStop, numThreads):
    print("\nnew thread started, thread number: " + str(numThreads) + "\n")
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
        shouldStop[0] = True
        print("\nServer no longer running\n")
        responseLines = "HTTP/1.1 200 OK\r\n"
        responseLines += "Connection: close\r\n"
        responseLines += "Content-Type: text/html" + "\r\n\r\n"
        content = open("./content/serverDoneRunning.html", 'rb').read()
        sendMessage(responseLines, content)
        return(0) #returning 0 will break out of the loop
    else:

        fileRequested = "./content/"+fileRequested

        contentType="error"

        try:
            contentType = fileRequested.split('.')[2]
        except:
            print("\nno content type found\n")

        print("\ncontent type: " + contentType)

        #set the right content type for the response header
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
        elif(contentType == "mp4"):
            contentType = "video/mp4"


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

numThreads = 0
while True:
    connection_socket, addr = server_socket.accept()
    numThreads += 1
    threading.Thread(target=clientThread, args=(connection_socket, shouldStop, numThreads,)).start()
    if(shouldStop[0]):
        break

server_socket.close()
