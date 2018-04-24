#20151535 Gunhoo Park
# NonBlockingTCPServer.py
#

from socket import *
from select import *
import datetime

serverPort = 21535
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
connectionList = [serverSocket]
clientList = []
countList = []
connectionNumber = 0
clientNumber = 0
print("The server is ready to receive on port", serverPort)

while connectionList:
    try:
        read_socket, write_socket, error_socket = select(connectionList, [], [])

        for sock in read_socket:
            if sock == serverSocket:
                clientNumber += 1
                connectionNumber += 1
                connectionSocket, clientAddress = serverSocket.accept()
                connectionList.append(connectionSocket)
                clientList.append(clientAddress)
                print('Client', clientNumber, ' is connected. Number of connected clients =', connectionNumber)
            else:
                myNumber = clientNumber
                data = sock.recv(2048)
                if data:
                    message = data.decode()
                    modifiedMessage = message.split('message')
                    if modifiedMessage[0] == '1':
                        sendingMessage = modifiedMessage[1].upper()
                        sock.send(sendingMessage.encode())
                        print('Connection requested from', clientList[myNumber-1])
                        print('Command 1')
                        continue
                    elif modifiedMessage[0] == '2':
                        sendingMessage = modifiedMessage[1].lower()
                        sock.send(sendingMessage.encode())
                        print('Connection requested from', clientList[myNumber-1])
                        print('command 2')
                        continue
                    elif modifiedMessage[0] == '3':
                        sendingMessage = clientList[myNumber-1][0] + 'port' + str(clientList[myNumber-1][1])
                        sock.send(sendingMessage.encode())
                        print('Connection requested from', clientList[myNumber-1])
                        print('command 3')
                        continue
                    elif modifiedMessage[0] == '4':
                        message = datetime.datetime.now()
                        modifiedMessage = message.strftime('%Y-%m-%d %H:%M:%S')
                        sock.send(modifiedMessage.encode())
                        print('Connection requested from', clientList[myNumber-1])
                        print('command 4')
                        continue
                    elif modifiedMessage[0] == '5':
                        connectionNumber -= 1
                        print('Client', myNumber, 'disconnected. Number of connected clients =', connectionNumber)
                        connectionList.remove(sock)
                        sock.close()
                        break
                    else :
                        connectionNumber -= 1
                        connectionList.remove(sock)
                        sock.close()
                        print('Client', myNumber, 'disconnected. Number of connected clients =', connectionNumber)
                        break
                else:
                    connectionList.remove(sock)
                    sock.close()
    except KeyboardInterrupt:
        print('Bye bye~')
        exit()
