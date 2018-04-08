# BasicTCPServer.py
#

from socket import *
import time
import datetime

serverPort = #server port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive on port", serverPort)

(connectionSocket, clientAddress) = serverSocket.accept()

while True:
    try:
        message = connectionSocket.recv(2048).decode()
        modifiedMessage = message.split('message')
        if modifiedMessage[0] == '1':
            sendingMessage = modifiedMessage[1].upper()
            connectionSocket.send(sendingMessage.encode())
            print('Connection requested from', clientAddress)
            print('Command 1')
            continue
        elif modifiedMessage[0] == '2':
            sendingMessage = modifiedMessage[1].lower()
            connectionSocket.send(sendingMessage.encode())
            print('Connection requested from', clientAddress)
            print('command 2')
            continue
        elif modifiedMessage[0] == '3':
            sendingMessage = clientAddress[0] + 'port' + str(clientAddress[1])
            connectionSocket.send(sendingMessage.encode())
            print('Connection requested from', clientAddress)
            print('command 3')
            continue
        elif modifiedMessage[0] == '4':
            message = datetime.datetime.now()
            modifiedMessage = message.strftime('%Y-%m-%d %H:%M:%S')
            connectionSocket.send(modifiedMessage.encode())
            print('Connection requested from', clientAddress)
            print('command 4')
            continue
        elif modifiedMessage[0] == '5':
            connectionSocket.close()
            (connectionSocket, clientAddress) = serverSocket.accept()
            continue
        else :
            connectionSocket.close()
            (connectionSocket, clientAddress) = serverSocket.accept()
            continue
    except KeyboardInterrupt:
        print('Bye bye~')
        exit()
