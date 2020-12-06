import socket

host = socket.gethostname()
port = 8000

s = socket.socket()
s.bind(host, port)

s.listen(1)
print("Waiting for client...")
client_socket, client_addr = s.accept()

print("Connection from ", str(client_addr))
while True:
    data = client_socket.recv(1024).decode('utf-8')
    print("Client> ", data)
    client_socket.send(data.encode('utf-8'))
    if not data:
        break
client_socket.close()