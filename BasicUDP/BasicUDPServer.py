# BasicUDPServer.py
#

from socket import *
import datetime

serverPort = #portnumber
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("The server is ready to receive on port", serverPort)

while True:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().split('message')
        if modifiedMessage[0] == '1':
            print('Connection requested from', clientAddress)
            print('Command 1')
            sendingMessage = modifiedMessage[1].upper()
            serverSocket.sendto(sendingMessage.encode(), clientAddress)
            continue
        elif modifiedMessage[0] == '2':
            print('Connection requested from', clientAddress)
            print('Command 2')
            sendingMessage = modifiedMessage[1].lower()
            serverSocket.sendto(sendingMessage.encode(), clientAddress)
            continue
        elif modifiedMessage[0] == '3':
            print('Connection requested from', clientAddress)
            print('Command 3')
            sendingMessage = clientAddress[0] + 'port' + str(clientAddress[1])
            serverSocket.sendto(sendingMessage.encode(), clientAddress)
            continue
        elif modifiedMessage[0] == '4':
            print('Connection requested from', clientAddress)
            print('Command 3')
            message = datetime.datetime.now()
            sendingMessage = message.strftime('%Y-%m-%d %H:%M:%S')
            serverSocket.sendto(sendingMessage.encode(), clientAddress)
            continue
        else :
           print('Wrong input from clinet:(')
           continue
    except KeyboardInterrupt :
        print('Bye bye~')
        exit()
