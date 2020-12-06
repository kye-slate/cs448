import sys
import hashlib
import csv
import secrets
import myserver
from getpass import getpass

seed_max_size = 100000000000000

filename = db_file = "user_db.csv"

def parser(query):
    query_args = query.split(" ")
    print("Query split: ", query_args)
    dispatcher = {
        "login"     : login,
        "quit"      : quitApp,
        "adduser"   : addUser,
        "invalid"   : invalid
    }
    dispatch = dispatcher.get(query_args[0], invalid)
    dispatch(query_args)
    
def login(args):
    print ("Logged into ", args)
    
    
def quitApp(args):
    sys.exit()
    
def addUser(args):
    username = args
    password = getpass("Password: ")
    repassword = getpass("Reenter Password: ")
    
    if (password == repassword):
        salt = secrets.randbelow(seed_max_size)
        input_string = username + password + str(salt)
        
        hash = hashlib.sha256(input_string.encode('utf-16'))
        
        file = open(filename, "a")
        file.write('\n' + username + ',' + str(hash.hexdigest()) + ',' + str(salt))
        file.close()
        

def invalid(args):
    print("Unrecognized command.")
    