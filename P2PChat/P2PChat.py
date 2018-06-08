


from socket import *
from threading import Thread
import threading
import sys, time

N = 4
K = 2
nodes = {1:('?.?.?.?', 21535), 2:('?.?.?.?', 31535), 3:('?.?.?.?', 41535), 4:('?.?.?.?', 51535)}
serverName = ''
serverSocket = socket(AF_INET, SOCK_DGRAM)

connected = {}
cTotal = 0
lock = threading.Lock()

if len(sys.argv) < 3:
    print("Usage : python3 P2PChat.py 1 ironman")
    exit()
else:
    nodeid = sys.argv[1]
    nickName = sys.argv[2]
    if int(nodeid)>4 or int(nodeid)<1:
        print("Node id's boundary is 1 to 4")
        exit()
    if nickName.isalpha() is False:
        print("Name must be English only")
        exit()
    if len(nickName) > 64:
        print("Length of your name must be under 64")
        exit()

if int(nodeid)==1:
    serverPort=21535
elif int(nodeid)==2:
    serverPort=31535
elif int(nodeid)==3:
    serverPort=41535
else:
    serverPort=51535

serverSocket.bind(('?.?.?.?', serverPort))
connected[int(nodeid)]= str(('?.?.?.?', serverPort))

def rcvMsg(sock):
    global connected, cTotal
    stack = []
    while True:
        try:
            receivedMessage = sock.recv(2048).decode()
            id = receivedMessage.split(">")
            src = receivedMessage.split(":")
            lock.acquire()
            # connection
            if src[0] == "ack" and src[1] not in connected.keys() and len(connected) < K and cTotal < N and src[1] != nodeid:
                connected[int(src[1])] = src[2]
                cTotal = cTotal + 1
                lock.release()
                continue
            # message from myself -> pass
            if src[0] != "ack" and src[1].split(">")[0] != nickName:
                if len(stack) == 0:
                    stack.append([int(src[0]), int(src[2])])
                    print(src[1])
                    for address in connected.values():
                        conAddr = str(address).split("'")[1]
                        conPort = str(address).split(", ")[1].split(")")[0]
                        serverSocket.sendto(receivedMessage.encode(), (conAddr, int(conPort)))
                else:s
                    # if message is already received
                    if [int(src[0]), int(src[2])] in stack:
                        pass
                    # if message is received first time
                    else:
                        print(src[1])
                        stack.append([int(src[0]), int(src[2])])
                        for address in connected.values():
                            conAddr = str(address).split("'")[1]
                            conPort = str(address).split(", ")[1].split(")")[0]
                            serverSocket.sendto(receivedMessage.encode(), (conAddr, int(conPort)))
            lock.release()
        except KeyboardInterrupt:
            print("Bye bye~~")
            pass

def runChat():
    global connected, cTotal
    cnum = 0
    seqno = 0
    connectionMessage = "ack:"+str(nodeid)+":"+str(serverSocket.getsockname())
    with serverSocket:
        newThread = Thread(target=rcvMsg, args=(serverSocket,))
        newThread.daemon = True
        print("Wait seconds to connect...")
        newThread.start()
        try:
            time.sleep(5)
            for key in nodes.keys():
                address = nodes.get(key)
                if str(address) not in connected.values() and cnum < K and cTotal < N:
                    connected[int(key)]=str(address)
                    cnum = cnum + 1
                    serverSocket.sendto(connectionMessage.encode(), address)
        except KeyboardInterrupt:
            serverSocket.close()
            print("bye bye!")
            exit()
        print("You are connected to the P2P world on ", serverSocket.getsockname())
        while newThread.isAlive():
            try:
                message = input()
                seqno = seqno + 1
                if message == "\quit":
                    serverSocket.close()
                    exit()
                if message == "\connection":
                    lock.acquire()
                    print(list(connected.items()))
                    lock.release()
                    continue
                modifiedMessage = nodeid+":"+nickName+">"+message+":"+str(seqno)
                lock.acquire()
                for address in connected.values():
                    conAddr = str(address).split("'")[1]
                    conPort = str(address).split(", ")[1].split(")")[0]
                    serverSocket.sendto(modifiedMessage.encode(), (conAddr, int(conPort)))
                lock.release()
            except error:
                print("bye~")
                serverSocket.close()
                exit()
            except KeyboardInterrupt:
                print("bye bye~~~")
                serverSocket.close()
                exit()

runChat()