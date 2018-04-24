# MultiThreadTCPServer.py
#

from socket import *
import datetime
import threading

connectionNumber = 0
clientNumber = 0

class ClientThread(threading.Thread):
    def __init__(self, clientAddrss, connectionSocket):
        threading.Thread.__init__(self)
        self.csocket = connectionSocket
        self.caddr = clientAddress
        global clientNumber, connectionNumber
        clientNumber += 1
        connectionNumber += 1
    def run(self):
        global clinetNumber, connectionNumber
        myNumber = clientNumber
        print("Client", clientNumber, "connected. Number of connected clients = ", connectionNumber)
        while True:
            try:
                message = self.csocket.recv(2048).decode()
                modifiedMessage = message.split('message')
                if modifiedMessage[0] == '1':
                    sendingMessage = modifiedMessage[1].upper()
                    self.csocket.send(sendingMessage.encode())
                    print('Connection requested from', self.caddr, 'client', myNumber)
                    print('Command 1')
                    continue
                elif modifiedMessage[0] == '2':
                    sendingMessage = modifiedMessage[1].lower()
                    self.csocket.send(sendingMessage.encode())
                    print('Connection requested from', self.caddr, 'client', myNumber)
                    print('command 2')
                    continue
                elif modifiedMessage[0] == '3':
                    sendingMessage = self.caddr[0] + 'port' + str(self.caddr[1])
                    self.csocket.send(sendingMessage.encode())
                    print('Connection requested from', self.caddr, 'client', myNumber)
                    print('command 3')
                    continue
                elif modifiedMessage[0] == '4':
                    message = datetime.datetime.now()
                    sendingMessage = message.strftime('%Y-%m-%d %H:%M:%S')
                    self.csocket.send(sendingMessage.encode())
                    print('Connection requested from', self.caddr, 'client', myNumber)
                    print('command 4')
                    continue
                elif modifiedMessage[0] == '5':
                    connectionNumber -= 1
                    print("Client", myNumber, "disconnected. Number of connected clients =", connectionNumber)
                    break
                else :
                    connectionNumber -= 1
                    print("Client", myNumber, "disconnected. Number of connected clients =", self.connectionNumber)
                    break
                self.csocket.close()
            except KeyboardInterrupt:
                self.csocket.close()
                connectionNumber -= 1
                print('Thread finish')

serverPort = 21535
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

print("The server is ready to receive on port", serverPort)
while True:
    try:
        serverSocket.listen(1)
        (connectionSocket, clientAddress) = serverSocket.accept()
        newThread = ClientThread(clientAddress, connectionSocket)
        newThread.start()
    except KeyboardInterrupt:
        connectionSocket.close()
        print('Bye bye~')
        exit()        
