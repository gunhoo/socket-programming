
# NetOmokClient.py
#

import socket, sys, datetime, os, time
from threading import Thread

serverName = #yourIPAddressserverPort = #yourPortNumber

#Handling clients argumnets
if len(sys.argv) < 2:
    print("Usage : python3 NetOmokClinet.py <NickName>")
    exit()
else:
    nickName = sys.argv[1]

myTurn = False
gameOn = False

#printing function
def rcvMsg(sock):
    global board, turn, gameOn, myTurn
    while True:
        try:
            data = sock.recv(1024).decode().split(':')
            if data[0] == '0':
                print(data[1])
                print('enter any key to exit')
                #return -1
                sys.exit(1)
            elif data[0] == '2':
                endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
                while True:
                    ans = input(data[1])
                    if datetime.datetime.now() > endTime:
                        print('time out! you have to answer in 10 sec')
                        rejectMsg = 'n'
                        sock.send(rejectMsg.encode())
                        break
                    if ans == 'y':
                        gameOn = True
                        myTurn = True
                        turn = 1
                        print_board(board)
                        print('game started. you play first.')
                        sock.send(ans.encode())
                        break
                    elif ans == "n":
                        sock.send(ans.encode())
                        break
                    else:
                        continue
                    break
            elif data[0] == '3':
                print(data[1])
                gameOn = True
                print_board(board)
                print('game started. '+data[2]+' plays first.')
                turn = 2
                continue
            elif data[0] == '5':
                play(int(data[1]),int(data[2]), int(data[3]))
                myTurn = True
                continue
            elif data[0] == '6':
                gameOn = False
                print(data[1])
                myTurn = False
                continue
            else:
                print(data[1])
            if not data:
                break
        except KeyboardInterrupt:
            print('Bye bye~')
            pass

turn = 0
#chatting and sending function
def runChat():
    global board, turn, gameOn, myTurn
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((serverName, serverPort))
            newThread = Thread(target=rcvMsg, args=(sock,))
            newThread.daemon = True
            newThread.start()
            sock.send(nickName.encode())
            while newThread.isAlive():
                try:
                    time.sleep(0.1)
                    msg = input()
                    modifiedMsg = msg.split(" ")
                    #message handling
                    if msg == '\quit':
                        sock.send(msg.encode())
                        sock.close()
                        break
                    elif modifiedMsg[0] == '\w' and len(modifiedMsg) < 3:
                        print("usage:\w <nickname> <message>\nenter message to whisper")
                        continue
                    elif modifiedMsg[0] == '\play':
                        sock.send(msg.encode())
                        continue
                    if modifiedMsg[0] == '\ss' and len(modifiedMsg) == 3:
                        #sock.send(msg.encode())
                        if gameOn:
                            if myTurn:
                                playResult = play(int(modifiedMsg[1]),int(modifiedMsg[2]), int(turn))
                                if playResult == -1:
                                    continue
                                elif playResult == 1:
                                    playMsg = msg+":"+str(turn)
                                    winMsg = playMsg+':win'
                                    sock.send(winMsg.encode())
                                    myTurn = False
                                    continue
                                else:
                                    playMsg = msg+":"+str(turn)
                                    sock.send(playMsg.encode())
                                    myTurn = False
                                    continue
                            else:
                                print('Not my turn')
                                continue
                        else:
                            print('Play game first:(')
                            continue
                    elif modifiedMsg[0] == '\gg':
                        if gameOn:
                            myTurn = False
                            ggMsg = '\gg '+nickName
                            sock.send(ggMsg.encode())
                            print('you lose')
                            continue
                        else:
                            print('Play game first:(')
                            continue
                    else:
                        sock.send(msg.encode())
                        continue
                except KeyboardInterrupt:
                    sock.close()
                    sys.exit(1)
            sys.exit(1)
        except KeyboardInterrupt:
            interruptMsg = '0:KeyboardInterrupt'
            sock.send(interruptMsg.encode())
            sock.close()
            print('Bye bye~')
        except Exception as e:
            interruptMsg = '0:KeyboardInterrupt'
            sock.send(interruptMsg.encode())
            sock.close()
        finally:
            print('bye bye~')
            sock.close()
            sys.exit(1)

ROW = 10
COL = 10

def print_board(b):

    print("   ", end="")
    for j in range(0, COL):
        print("%2d" % j, end="")

    print()
    print("  ", end="")
    for j in range(0, 2*COL+3):
        print("-", end="")
    
    print()
    for i in range(0, ROW):
        print("%d |" % i, end="")
        for j in range(0, COL):
            c = b[i][j]
            if c == 0:
                print(" +", end="")
            elif c == 1:
                print(" 0", end="")
            elif c == 2:
                print(" @", end="")
            else:
                print("ERROR", end="")
        print(" |")

    print("  ", end="")
    for j in range(0, 2*COL+3):
        print("-", end="")
    
    print()

def check_win(x, y):
    global board
    b = board
    last_stone = b[x][y]
    start_x, start_y, end_x, end_y = x, y, x, y

    # check x
    while (start_x - 1 >= 0 and
            b[start_x - 1][y]  == last_stone):
        start_x -= 1
    while (end_x + 1 < ROW and
            b[(end_x + 1)][y] == last_stone):
        end_x += 1
    if end_x - start_x + 1 >= 5:
        return last_stone

    # check y
    start_x, start_y, end_x, end_y = x, y, x, y
    while (start_y - 1 >= 0 and
            b[x][start_y - 1] == last_stone):
        start_y -= 1
    while (end_y + 1 < COL and
            b[x][end_y + 1] == last_stone):
        end_y += 1
    if end_y - start_y + 1 >= 5:
        return last_stone
    
    # check diag 1
    start_x, start_y, end_x, end_y = x, y, x, y
    while (start_x - 1 >= 0 and start_y - 1 >= 0 and
            b[start_x - 1][start_y - 1] == last_stone):
        start_x -= 1
        start_y -= 1
    while (end_x + 1 < ROW and end_y + 1 < COL and
            b[end_x + 1][end_y + 1] == last_stone):
        end_x += 1
        end_y += 1
    if end_y - start_y + 1 >= 5:
        return last_stone
    
    # check diag 2
    start_x, start_y, end_x, end_y = x, y, x, y
    while (start_x - 1 >= 0 and end_y + 1 < COL and
            b[start_x - 1][end_y + 1] == last_stone):
        start_x -= 1
        end_y += 1
    while (end_x + 1 < ROW and start_y - 1 >= 0 and
            b[end_x + 1][start_y - 1] == last_stone):
        end_x += 1
        start_y -= 1
    if end_y - start_y + 1 >= 5:
        return last_stone
    
    return 0

board = [[0 for row in range(ROW)] for col in range(COL)]

def play(x, y, t):
    global board, ROW, COL, turn
    count, win = 0, 0
    if x < 0 or y < 0 or x >= ROW or y >= COL:
        print("error, out of bound!")
        #time.sleep(2)
        return -1
    elif board[x][y] != 0:
        print("error, already used!")
        #time.sleep(2)
        return -1
    if t == 1:
        board[x][y] = 1
    else:
        board[x][y] = 2
    print_board(board)
    win = check_win(x, y)
    if win != 0 and turn == t:
        print('you win!')
        return 1
    if win != 0 and turn != t:
        print("you lose!")
        return 1 
     
    count += 1
    if count == ROW*COL:
       return -1
    
    return 0

runChat()
