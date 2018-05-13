# socket programming

All program should be filled with your own server name and port numbers both server side and client side.


How to compile and run
    1. In Linux environment, you have to compile and run with python3.
    2. Fill up the code with your own server IP address and PORT numbers.
    3. Run the server first, then run client.
    4. If you use NetOmokClient, you shold use nickname and compile as 'python3 NetOmokClient Alice'

In 'BasicTCP', 'BasicUDP', 'MultiThreadTCP', and 'NonBlockingTCP' directory
There are 4 commmands in client:
    1. '1' // convert text to UPPER-case
    2. '2' // convert text to lower-case
    3. '3' // get my IP address and port number
    4. '4' // get server time

In 'NetOmok' directory
There are many commands in client:
    0. Chat function with all users is provided by default
    1. '\list' // show the <nickname, IP, Port> list of all users
    2. '\w <nickname> <message>' // whisper to <nickname>
    3. '\quit' // disconnect from server, and quit
    4. '\play <nickname>' // ask <nickname> to play omok game
    5. '\ss <x> <y>' // put your stone at <x>, <y> position
    6. '\gg' // give up game