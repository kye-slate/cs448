import socket
import secrets
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet

host = socket.gethostname()
port = 8080

s = socket.socket()
s.connect((host, port))

key = s.recv(1024)
codec = Fernet(key)


msg = ""
while (msg != 'q'):
    msg = input("client> ")
    s.send(codec.encrypt(msg.encode('utf-8')))
   
    if msg == 'q': break

    output = ""
    while (output != msg):
        output = s.recv(1024)
        output = codec.decrypt(output).decode('utf-8')
        
        outputS = output.split(';')
        
        if outputS[0] == "0":
            print("Server says: Success")
        elif outputS[0] == "1":
            print("Server says: Failure")
        elif outputS[0] == "2":
            password = getpass(outputS[1])
            s.send(codec.encrypt(password.encode('utf-8')))
        elif outputS[0] == "3":
            print("Server says: ", outputS[1])
        elif outputS[0] == "69":
            print("Server says: ", outputS[1])
s.close()