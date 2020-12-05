import socket

host = socket.gethostname()
port = 8080

s = socket.socket()
s.connect((host, port))

msg = ""
while (msg != 'q'):
    msg = input("client> ")
    s.send(msg.encode('utf-8'))
    print("Server says: ", s.recv(1024).decode('utf-8'))
s.close()