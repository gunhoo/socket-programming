
# NetOmokServer.py
#

from socket import *
import threading
import sys

lock = threading.Lock()
clients={}
players={}
gameOn = False

class ClientThread(threading.Thread):
    #constructor
    def __init__(self, clientAddress, connectionSocket, clientName):
        threading.Thread.__init__(self)
        self.clientName = clientName
        self.csock = connectionSocket
        self.caddr = clientAddress
    #When clients are added
    def addClient(self, clientName, connnectionSocket, clientAddress):
        global clients
        if clientName in clients:
            rejectMessage = "0:duplicate nickname. cannot connect"
            connectionSocket.send(rejectMessage.encode())
            connectionSocket.close()
            return
        lock.acquire()
        clients[clientName] = (connectionSocket,clientAddress, clientName)
        lock.release()
    #When clients are removed
    def removeClient(self, clientName):
        global clients, clientNumber,gameOn, players
        if clientName not in clients:
            return
        lock.acquire()
        clientNumber -= 1
        if clientName in players:
            gameOn = False
            del players[clientName]
        del clients[clientName]
        lock.release()
    def messageHandler(self, clientName, msg):
        global gameOn,clients,players
        modifiedMsg = msg.split(" ")
        i=2
        whispMsg = ""
        while i<len(modifiedMsg):
            whispMsg += modifiedMsg[i]+" "
            i += 1
        playMsg = msg.split(":")
        if msg == "\quit":
            return -1
        elif msg == "0:KeyboardInterrupt":
            return -1
        elif msg == "\list":
            self.sendList()
        elif modifiedMsg[0] == "\w":
            self.sendWishperMessage(clientName,modifiedMsg[1], whispMsg)
        elif modifiedMsg[0] == "\play":
            if self.requestGame(clientName, modifiedMsg[1]) == -1:
                alreadyPlayMsg = "4:Someone are already playing...:("
                self.csock.send(alreadyPlayMsg.encode())
        elif modifiedMsg[0] == '\ss' and len(modifiedMsg[2].split(':')) == 2:
            rcvdTurn = modifiedMsg[2].split(':')
            self.putStone(clientName, modifiedMsg[1],modifiedMsg[2],rcvdTurn[1])
        elif modifiedMsg[0] == '\ss' and modifiedMsg[2].split(':')[2] == 'win':
            gameOn = False
            rcvdTurn = modifiedMsg[2]
            self.putStone(clientName, modifiedMsg[1], modifiedMsg[2], rcvdTurn) 
        elif modifiedMsg[0] == '\gg':
            gameOn = False
            lock.acquire()
            for player1, player2 in players.values():
                if player1 == modifiedMsg[1]:
                    for clientSocket, clientAddress, clientName in clients.values():
                        if player2 == clientName:
                            ggMsg = '6:'+modifiedMsg[1]+' gave up. you win!'
                            clientSocket.send(ggMsg.encode())
                            break
                elif player2 == modifedMsg[1]:
                    for clientSocket, clientAddress, clientName in clients.values():
                        if player2 == clientName:
                            ggMsg = '6:'+modifiedMsg[1]+'gave up. you win!'
                            clientSocket.send(ggMsg.encode())
                            break
            lock.release()
        else:
            sendingMsg = '1:'+clientName+'>'+msg
            self.sendMessageToAll(sendingMsg, clientName)
        return 1
    #When client inputs \list function
    def sendList(self):
        global clients
        sendingMsg = '1:'
        lock.acquire()
        for clientSocket, clientAddress, clientName in clients.values():
            sendingMsg += '<'+clientName+','+str(clientAddress)+'>\n'
        self.csock.send(sendingMsg.encode())
        lock.release()
    #When clinet wants to whispering
    def sendWishperMessage(self,sender,nickName,msg):
        global clients
        sendingMsg = "1:"+sender+">>"+msg
        lock.acquire()
        for clientSocket, clientAddress, clientName in clients.values():
            if clientName == nickName:
                clientSocket.send(sendingMsg.encode())
                break
        lock.release()
    def putStone(self, sender, x, y, rcvdTurn):
        global clients, players
        sendingMsg = '5:'+x+':'+y
        for player1, player2 in players.values():
            if player1 == sender:
                lock.acquire()
                for clientSocket, clientAddress, clientName in clients.values():
                    if player2 == clientName:
                        sendingMsg += ':'+rcvdTurn
                        clientSocket.send(sendingMsg.encode())
                        break
                lock.release()
                break
            else:
                lock.acquire()
                for clientSocket, clientAddress, clientName in clients.values():
                    if player1 == clientName:
                        sendingMsg += ':'+rcvdTurn
                        clientSocket.send(sendingMsg.encode())
                        break
                lock.release()
                break
#When game is end, then gameOn should be False
    #play omok game
    def requestGame(self, sender, receiver):
        global gameOn, clients, players
        if gameOn:
            return -1
        else:
            sendingMsg = '2:'
            lock.acquire()
            for clientSocket, clientAddress, clientName in clients.values():
                if receiver == clientName:
                    sendingMsg += sender+' wants to play with you. agree?[y/n]:'
                    clientSocket.send(sendingMsg.encode())
                    rcvMsg = clientSocket.recv(128).decode()
                    playMsg = "3:game start!\n:"+clientName
                    rejectMsg = '30:cannot make play request!'
                    if rcvMsg[0] == 'y':
                        gameOn = True
                        self.csock.send(playMsg.encode())
                        players[sender] = {sender, receiver}
                        break
                    else:
                        self.csock.send(rejectMsg.encode())
                        break
                    break
            lock.release()
        return 1
    #sending message to all except sender
    def sendMessageToAll(self, msg, nickName):
        global clients
        lock.acquire()
        for connectionSocket, clientAddress, clientName in clients.values():
            if clientName != nickName:
                connectionSocket.send(msg.encode())
        lock.release()
    #Decide whether client have qaulification to enter or not
    def user(self):
        global nickName, clientNumber, clients
        nickName = []
        if clientNumber > 6:
            rejectMessage = "0:full. cannot connect"
            self.csock.send(rejectMessage.encode())
            self.csock.close()
            return -1
        elif self.clientName in clients:
            rejectMessage = "0:duplicate nickname. cannot connect"
            self.csock.send(rejectMessage.encode())
            self.csock.close()
            return -1
        elif self.clientName.isalpha() is False:
            rejectMessage = "0:nickname must be English only"
            self.csock.send(rejectMessage.encode())
            self.csock.close()
            return -1
        else:
            clientNumber += 1
            nickName.append(self.clientName)
            helloMessage = "1:welcome "+self.clientName+" to net omok chat room at "+str(serverAddress)+". you are "+str(clientNumber)+"th user"
            self.csock.send(helloMessage.encode())
            print("welcome", self.clientName)
            return 1
    def run(self):
        global clientNumber, clients
        myNumber = clientNumber
        if self.user() == -1:
            return
        self.addClient(self.clientName,self.csock,self.caddr)
        try:
            msg = self.csock.recv(1024)
            while msg:
                print(self.clientName,msg.decode())
                if self.messageHandler(self.clientName, msg.decode()) == -1:
                    self.csock.close()
                    break
                msg = self.csock.recv(1024)
        except Exception as e:
            print(e)
        print(self.clientName+" disconnected. There are "+str(len(clients)-1)+" users now")
        self.removeClient(self.clientName)
        #print(self.clientName+" disconnected. There are "+str(len(clients)-1)+" users now")
    def interrupt(self):
        interruptMsg = "0:server is interrupted"
        lock.acquire()
        for clientSocket, clientAddress, clientName in clients.values():
            clientSocket.send(interruptMsg.encode())
            clientSocket.close()
        lock.release()
 
serverPort = #yourPortNumber
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverAddress = serverSocket.getsockname()
connectionNumber = 0
clientNumber = 0
print("The server is ready to receive on",serverAddress)

serverSocket.listen(1)
#keyboard interrupt handler when no one connected at first time
try:
    (connectionSocket, clientAddress) = serverSocket.accept()
    clientName = connectionSocket.recv(512).decode()
    newThread = ClientThread(clientAddress, connectionSocket, clientName)
except KeyboardInterrupt: # nothing to close of threads
    print('Bye bye~')
#    connectionSocket.close()
    exit()
try:
    while True:
        newThread.start()
        serverSocket.listen(1)
        (connectionSocket, clientAddress) = serverSocket.accept()
        clientName = connectionSocket.recv(512).decode()
        newThread = ClientThread(clientAddress, connectionSocket, clientName)
except KeyboardInterrupt:
    newThread.interrupt()
    print('Wait until clients finsish the system...')
    try:
#        lock.release()
        newThread.terminate()
        serverSocket.close()
    except RuntimeError:
        serverSocket.close()
        exit()
    finally:
        serverSocket.close()
        print('Bye bye~')
        exit()
