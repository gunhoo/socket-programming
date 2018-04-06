
# BasicUDPClient.py
#

from socket import *
import time

serverName = #servername
serverPort = #portnumber

clientSocket = socket(AF_INET, SOCK_DGRAM)
#clientSocket.bind(('', 5432))

print("The client is running on port", clientSocket.getsockname()[1])
while True:
    try:
        print('')
        print('Menu')
        print('1) convert text to UPPER-case')
        print('2) convert text to LOWER-case')
        print('3) get my IP address and port number')
        print('4) get server time')
        print('5) exit')
        option = input('Input option: ')
        if option == '1':
            message = input('Input lowercase sentence: ')
            modifiedMessage = option
            modifiedMessage += 'message'
            modifiedMessage += message
            start_time = time.time()
            clientSocket.sendto(modifiedMessage.encode(), (serverName, serverPort))

            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            end_time = time.time()

            print('Reply from server:', modifiedMessage.decode())
            print('Response time: ', (end_time - start_time)*1000, 'ms')

            continue
        elif option == '2':
            message = input('Input uppercase sentence: ')
            modifiedMessage = option
            modifiedMessage += 'message'
            modifiedMessage += message
            start_time = time.time()
            clientSocket.sendto(modifiedMessage.encode(), (serverName, serverPort))

            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            end_time = time.time()

            print('Reply from server:', modifiedMessage.decode())
            print('Response time: ', (end_time - start_time)*1000, 'ms')

            continue
        elif option == '3':
            start_time = time.time()
            clientSocket.sendto(option.encode(), (serverName, serverPort))
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            end_time = time.time()
            ipMessage = modifiedMessage.decode().split('port')
            print('Reply from server: IP =', ipMessage[0], 'port=', ipMessage[1])
            print('Response time: ', (end_time - start_time)*1000, 'ms')
            continue
        elif option == '4':
            start_time = time.time()
            clientSocket.sendto(option.encode(), (serverName, serverPort))
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            end_time = time.time()
            print('Reply form server: time =', modifiedMessage.decode())
            print('Response time: ', (end_time - start_time)*1000, 'ms')
            continue
        elif option == '5':
            print('Bye bye~')
            break
        else :
            print('Input error')
            continue
    except KeyboardInterrupt:
        print('')
        print('Bye bye~') 
        exit()
