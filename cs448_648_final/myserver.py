import socket
import hashlib
import csv
import secrets
from cryptography.fernet import Fernet


seed_max_size = 100000000000000
filename = db_file = "user_db.csv"

host = socket.gethostname()
port = 8080

s = socket.socket()
s.bind((host, port))

s.listen(1)
print("Waiting for client...")

# Client connect and key exchange
client_socket, client_addr = s.accept()
key = Fernet.generate_key()
codec = Fernet(key)

client_socket.send(key)


user = "Not logged in"

print("Connection from ", str(client_addr))
while True:
    data = client_socket.recv(1024)
    input = codec.decrypt(data).decode('utf-8')
   # print(data, input)
    inputS = input.split(' ')
    print("Client> ", inputS[0])
    
    if input == "q": break
    
    elif inputS[0] == "help":
        usage = "3;\n\nUsage:\n help\n login <username>\n whoami\n\n"
        usage = usage + "Admin:\n adduser <username>\n\n"
        usage = usage + "User:\n upload <file>.txt"
        client_socket.send(codec.encrypt(usage.encode('utf-8')))
   
    elif inputS[0] == "whoami":
        client_socket.send(codec.encrypt(("69;" + user).encode('utf-8')))
    
    if (len(inputS) == 2):
    
        if (inputS[0] == "login"):
            user = inputS[1]

            client_socket.send(codec.encrypt("2;Password: ".encode('utf-8')))
            password = codec.decrypt(client_socket.recv(1024)).decode('utf-8')

            db_row = False
            try:
                with open(filename, newline='') as db:
                    csv_reader = csv.reader(db)
                    for row in csv_reader:
                        if user == row[0]: db_row = row
            except:
                print ("ERROR: Unable to open file ", filename)
                break
            if not db_row: break
            
            input_string = ""
            input_string = user + password + str(db_row[2])
            
            hash = hashlib.sha256(input_string.encode('utf-16'))
            
            if (db_row[1] != str(hash.hexdigest())): 
                client_socket.send(codec.encrypt("1;failure".encode('utf-8')))
            else:
                client_socket.send(codec.encrypt("0;success".encode('utf-8')))


        elif (inputS[0] == "adduser"):
            if user == "admin":
                username = inputS[1]

                client_socket.send(codec.encrypt("2;Password: ".encode('utf-8')))
                password = codec.decrypt(client_socket.recv(1024).decode('utf-8'))

                client_socket.send(codec.encrypt("2;Reenter Password: ".encode('utf-8')))
                repassword = codec.decrypt(client_socket.recv(1024).decode('utf-8'))

                if (password == repassword):
                    salt = secrets.randbelow(seed_max_size)
                    input_string = username + password + str(salt)

                    hash = hashlib.sha256(input_string.encode('utf-16'))

                    file = open(filename, "a")
                    file.write('\n' + username + ',' + str(hash.hexdigest()) + ',' + str(salt))
                    file.close()
                    client_socket.send(codec.encrypt("0".encode('utf-8')))
                else: client_socket.send(codec.encrypt("1".encode('utf-8')))
            else:
                client_socket.send(codec.encrypt("1".encode('utf-8')))
                
    client_socket.send(codec.encrypt(input.encode('utf-8')))
    
    if not data:
        break
client_socket.close()