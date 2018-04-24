# BasicTCPClient.py
#

from socket import *
import time

serverName = 'nsl2.cau.ac.kr'
serverPort = 21535

clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((serverName, serverPort))
except Exception as e:
    print('Cannot connect to the server')
    exit()

print("The client is running on port", clientSocket.getsockname()[1])

while True :
    try:
        print('')
        print('<Menu>')
        print('1) convert text to UPPER-case')
        print('2) convert text to LOWER-case')
        print('3) get my IP address and port number')
        print('4) get server time')
        print('5) exit')
        option = input('Input option: ')
        if option == '1':
            message = input('Input lowercase sentence: ')
            print('')
            modifiedMessage = option + 'message' + message
            start_time = time.time()
            clientSocket.send(modifiedMessage.encode())
            receivedMessage = clientSocket.recv(2048)
            end_time = time.time()
            print('Reply from server:', receivedMessage.decode())
            print('Response time : ', (end_time - start_time)*1000, 'ms')
            continue
        elif option == '2':
            message = input('Input uppercase sentence: ')
            print('')
            modifiedMessage = option + 'message' + message
            start_time = time.time()
            clientSocket.send(modifiedMessage.encode())
            receivedMessage = clientSocket.recv(2048)
            end_time = time.time()
            print('Relpy from server:', receivedMessage.decode())
            print('Response time : ', (end_time - start_time)*1000, 'ms')
            continue
        elif option == '3':
            print('')
            start_time = time.time()
            clientSocket.send(option.encode())
            ipMessage = clientSocket.recv(2048)
            end_time = time.time()
            modifiedMessage = ipMessage.decode().split('port')
            print('Reply from server: IP =', modifiedMessage[0], 'port=', modifiedMessage[1])
            print('Response time: ', (end_time - start_time)*1000, 'ms' )
            continue
        elif option == '4':
            print('')
            start_time = time.time()
            clientSocket.send(option.encode())
            modifiedMessage = clientSocket.recv(2048)
            end_time = time.time()
            print('Reply from server: time =', modifiedMessage.decode())
            print('Response time: ', (end_time - start_time)*1000, 'ms')
            continue
        elif option == '5':
            clientSocket.send(option.encode())
            print('Bye bye~')
            break
        else :
            print('Input error')
            continue
        clientSocket.close()
    except KeyboardInterrupt:
        print('')
        print('Bye bye~')
        clientSocket.send(str(5).encode())
        clientSocket.close()
        exit()
