import socket
import os
import hashlib
import csv
import secrets
import shutil
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
usage = "3;\n\nUsage:\n help\n login <username>\n whoami\n q\n\n"
usage = usage + "Admin:\n adduser <username>\n remove <username>\n listall\n\n"
usage = usage + "User:\n display <file>.txt (only 'log' is viable)\n change password\n"


print("Connection from ", str(client_addr))
while True:
    data = client_socket.recv(1024)
    input = codec.decrypt(data).decode('utf-8')
   # print(data, input)
    inputS = input.split(' ')
    print("Client> ", input)
    
    if input == "q": break
    
    elif inputS[0] == "help":
        client_socket.send(codec.encrypt(usage.encode('utf-8')))
   
    elif inputS[0] == "whoami":
        client_socket.send(codec.encrypt(("69;" + user).encode('utf-8')))
    
    elif (input == "logout"):
        if user != "Not logged in":  
            user = "Not logged in"
            client_socket.send(codec.encrypt("69;Logged Out".encode('utf-8')))
    elif input == "listall":
        if user == "admin":
            file = open("user_db.csv")

            count = 0
            for line in file:
                count = count + 1
                client_socket.send(codec.encrypt(("69;"+line.split(',')[0]).encode('utf-8')))
            client_socket.send(codec.encrypt(("69;"+("Total Users: " + str(count))).encode('utf-8')))    
            
            file.close()
    if (len(inputS) == 2):
    
        if (inputS[0] == "login"):
            username = inputS[1]

            client_socket.send(codec.encrypt("2;Password: ".encode('utf-8')))
            password = codec.decrypt(client_socket.recv(1024)).decode('utf-8')

            db_row = False
            try:
                with open(filename, newline='') as db:
                    csv_reader = csv.reader(db)
                    for row in csv_reader:
                        if username == row[0]: db_row = row
            except:
                print ("ERROR: Unable to open file ", filename)
            if db_row != False:            
                input_string = ""
                input_string = username + password + str(db_row[2])
                
                hash = hashlib.sha256(input_string.encode('utf-16'))
                
                if (db_row[1] != str(hash.hexdigest())): 
                    client_socket.send(codec.encrypt("1;failure".encode('utf-8')))
                else:
                    client_socket.send(codec.encrypt("0;success".encode('utf-8')))
                    user = username
            else: client_socket.send(codec.encrypt("3;Incorrect Pass or Username".encode('utf-8')))
                    
        elif (inputS[0] == "adduser"):
            if user == "admin":
                file = open("user_db.csv")
                duplicate = False
                count = 0
                for line in file:
                    count = count + 1
                    if inputS[1] == line.split(',')[0]: duplicate = True
                file.close()
                
                if duplicate == False:
                    
                    username = inputS[1]

                    client_socket.send(codec.encrypt("2;Password: ".encode('utf-8')))
                    password = codec.decrypt(client_socket.recv(1024)).decode('utf-8')
                    client_socket.send(codec.encrypt("2;Reenter Password: ".encode('utf-8')))
                    repassword = codec.decrypt(client_socket.recv(1024)).decode('utf-8')

                    if (password == repassword):
                        salt = secrets.randbelow(seed_max_size)
                        input_string = username + password + str(salt)

                        hash = hashlib.sha256(input_string.encode('utf-16'))

                        file = open(filename, "a+")
                        file.write("\n" + username + ',' + str(hash.hexdigest()) + ',' + str(salt))
                        file.close()
                        
                        client_socket.send(codec.encrypt("0".encode('utf-8')))
                        
                        client_socket.send(codec.encrypt("3;Creating Directory...".encode('utf-8')))
                        cwd = os.getcwd()
                        
                        path = os.path.join(cwd, username)
                        try: 
                            os.mkdir(path)
                            client_socket.send(codec.encrypt("0;Success".encode('utf-8')))
                        except OSError as error:
                            client_socket.send(codec.encrypt("1;Failure".encode('utf-8')))
                        
                    else: client_socket.send(codec.encrypt("1".encode('utf-8')))
            else:
                client_socket.send(codec.encrypt("69;Failure - Not Admin".encode('utf-8')))
        
        elif (input == "change password"):
            
            username = user
                
            file = open(filename, 'r')
            list = file.read()
                
            file.close()
                
            list = list.split('\n')

            client_socket.send(codec.encrypt("2;Password: ".encode('utf-8')))
            password = codec.decrypt(client_socket.recv(1024)).decode('utf-8')
            client_socket.send(codec.encrypt("2;Reenter Password: ".encode('utf-8')))
            repassword = codec.decrypt(client_socket.recv(1024)).decode('utf-8')

                
            db_row = False
            count = 0
            with open(filename, newline='') as db:
                csv_reader = csv.reader(db)
                for row in csv_reader:
                    if username == row[0]: 
                        db_row = row
                    if db_row == False: count = count + 1
                
            if (db_row != False) and (password == repassword):
                input_string = ""
                input_string = username + password + str(db_row[2])
                    
                hash = hashlib.sha256(input_string.encode('utf-16'))
                    
                if (db_row[1] == str(hash.hexdigest())):
                    client_socket.send(codec.encrypt("2;Enter New Password:".encode('utf-8')))
                    password = codec.decrypt(client_socket.recv(1024)).decode('utf-8')
                    client_socket.send(codec.encrypt("2;Re-enter New Password:".encode('utf-8')))
                    repassword = codec.decrypt(client_socket.recv(1024)).decode('utf-8')

                    if (password == repassword):      
                        salt = secrets.randbelow(seed_max_size)
                        input_string = username + password + str(salt)
                        
                        hash = hashlib.sha256(input_string.encode('utf-16'))
                            
                        list[count] = username + ',' + str(hash.hexdigest()) + ',' + str(salt)
                            
                        file = open(filename, 'w')
                        for x in list:
                            file.write(x + '\n')
                        file.close()
                        client_socket.send(codec.encrypt("0".encode('utf-8')))
                    else: client_socket.send(codec.encrypt("1".encode('utf-8')))
        elif (inputS[0] == "remove"):
            if user == "admin":
                username = inputS[1]
                    
                file = open(filename, 'r')
                list = file.read()
                    
                file.close()
                    
                list = list.split('\n')
                    
                db_row = False
                count = 0
                with open(filename, newline='') as db:
                    csv_reader = csv.reader(db)
                    for row in csv_reader:
                        if username == row[0]: 
                            db_row = row
                        if db_row == False: count = count + 1
                               
                    
                index = 0
                file = open(filename, 'w')
                for x in list:
                    if index != count:
                        file.write(x + '\n')
                    index = index + 1
                file.close()
                
                # Delete User directory
                shutil.rmtree(username)
        elif (inputS[0] == "display"):
            if user != "Not logged in":
                f = inputS[1]
                        
                file = open(user + "/" + f, 'r')
                list = file.read()
                file.close()
                list = list.split('\n')
                        
                for x in list:
                    print(x)
                    client_socket.send(codec.encrypt(("69;" + x).encode('utf-8')))
                client_socket.send(codec.encrypt(("69;\n").encode('utf-8')))
            else: client_socket.send(codec.encrypt("1".encode('utf-8')))   
        else: client_socket.send(codec.encrypt("1".encode('utf-8')))
    #else: client_socket.send(codec.encrypt(usage.encode('utf-8')))
    
    if user != "Not logged in":  
        file = open(user + "\\log.txt", "a+")
        file.write("\n" + input)
        file.close()

    # Reset loop
    client_socket.send(codec.encrypt(input.encode('utf-8')))
    
    if not data:
        break
client_socket.close()