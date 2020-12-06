import socket
import parse
import hashlib
import csv
import secrets

seed_max_size = 100000000000000
filename = db_file = "user_db.csv"

host = socket.gethostname()
port = 8080

s = socket.socket()
s.bind((host, port))

s.listen(1)
print("Waiting for client...")
client_socket, client_addr = s.accept()

user = ""

print("Connection from ", str(client_addr))
while True:
    data = client_socket.recv(1024).decode('utf-8')
    input = data
    inputS = input.split(' ')
    print("Client> ", data)
    
    if inputS[0] == "help":
        usage = "\n\nUsage:\nlogin <username>\nadduser <username>\n"
        client_socket.send(usage.encode('utf-8'))
    elif inputS[0] == "whoami":
        client_socket.send(username.encode('utf-8'))
    if (len(inputS) == 2):
    
        if (inputS[0] == "login"):
            user = inputS[1]
        
            client_socket.send("2;Password: ".encode('utf-8'))
            password = client_socket.recv(1024).decode('utf-8')
            
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
            
            if (db_row[1] != str(hash.hexdigest())): user = ""
            
            
        elif (inputS[0] == "adduser"):
            if user == "admin":
                username = inputS[1]
                
                client_socket.send("2;Password: ".encode('utf-8'))
                password = client_socket.recv(1024).decode('utf-8')
                
                client_socket.send("2;Reenter Password: ".encode('utf-8'))
                repassword = client_socket.recv(1024).decode('utf-8')

                if (password == repassword):
                    salt = secrets.randbelow(seed_max_size)
                    input_string = username + password + str(salt)
                        
                    hash = hashlib.sha256(input_string.encode('utf-16'))
                        
                    file = open(filename, "a")
                    file.write('\n' + username + ',' + str(hash.hexdigest()) + ',' + str(salt))
                    file.close()
                    client_socket.send("0".encode('utf-8'))
                else: client_socket.send("1".encode('utf-8'))
            else:
                client_socket.send("1".encode('utf-8'))
                
            
    client_socket.send(data.encode('utf-8'))
    
    if not data:
        break
client_socket.close()