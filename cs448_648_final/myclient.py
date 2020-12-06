import socket
import secrets
import hashlib
from getpass import getpass

host = socket.gethostname()
port = 8080

s = socket.socket()
s.connect((host, port))

msg = ""
while (msg != 'q'):
    msg = input("client> ")
    s.send(msg.encode('utf-8'))
   
    output = ""
    while (output != msg):
        output = s.recv(1024).decode('utf-8')
      
        outputS = output.split(';')
        
        if outputS[0] == "0":
            print("Server says: Success")
        elif outputS[0] == "1":
            print("Server says: Failure")
        elif outputS[0] == "2":
            password = getpass("\n" + outputS[1])
            s.send(password.encode('utf-8'))
s.close()