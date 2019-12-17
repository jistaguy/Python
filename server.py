import socket
import sys
import os
import colorama
import json
colorama.init(autoreset=True)

class Service():
    def __init__(self):
        self.host=socket.gethostbyname(socket.gethostname())
        self.port=31415
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
        self.sock.bind((self.host,self.port))
        self.sock.listen()
        print(colorama.Fore.GREEN+'listening on', (self.host, self.port))

    def database(self):
        while True:
            try:
                self.db = input('Enter your database storage, last character should be \:')
                self.db = self.db.replace('\\','/',-1)
            except:
                print('Something unexpected happen , try again')
            else:
                if '/' == self.db[len(self.db)-1]:
                    break
                else:
                    continue
class Header():
    #underline Mechanism for files transfer:
    def __init__(self,file_size=0,file_name=0,recv_data=0,send_data=0):
        self.file_size=file_size
        self.file_name=file_name
        self.recv_data=recv_data
        self.send_data=send_data

def convert_to_dict(obj):
    #Part 1 of the Mechanism to transfer custom object via network 
    obj_dict={"__class__":obj.__class__.__name__}
    obj_dict.update(obj.__dict__)

    return obj_dict

def dict_to_obj(obj_dict):
    #Part 3 of the Mechanism to transfer custom object via network
    if "__class__" in obj_dict:
        class_name = obj_dict.pop('__class__')
    

    message_header = eval(class_name)(**obj_dict)
    
    return message_header

def file_preparation():
    #windows path correction for best compatability
    while True:
        try:
            file_name=input('Enter file name including extension: ')
        except:
            print(colorama.Fore.GREEN+'something wrong has been placed , try again')
        else:
            if '.' not in file_name:
                continue
            else:
                break
    return file_name

def helpmesir(client):
    command_reference = 'u - for uploading a file\nd - for downloading a file \nl - list database\ne - for closing the session'.encode('utf-8')
    client.sendall(command_reference)

def db_list():
    files_desc = os.listdir(srv.db)
    files_desc_s = ''

    for file_desc in files_desc:
        files_desc_s += file_desc+'\n'
    return files_desc_s.encode('utf-8')

def download(client):
    #App header creation for the file
    message_header = client.recv(4096).decode('utf-8')
    message_header = json.loads(message_header)
    message_header = dict_to_obj(message_header)

    #data storage unit
    file_data = b''

    #actual Data 
    while message_header.file_size > message_header.recv_data:
        file_data += client.recv(4096)
        message_header.recv_data = sys.getsizeof(file_data)
    
    #saving the transfered data
    open(srv.db + message_header.file_name , mode='wb').write(file_data)
    print(colorama.Fore.RED+'Transfer has been completed')

def upload(client):
    #file name that choosed to be downloded by user
    file_name = client.recv(4096).decode('utf-8')
    
    #actual file data
    local_file = open(srv.db+file_name , mode='rb' ).read()

    #Header creation and transfer preparation
    message_header = Header(len(local_file),file_name)
    message_header = convert_to_dict(message_header)
    message_header = json.dumps(message_header).encode('utf-8')

    #Object transfer
    client.sendall(message_header)

    #data file 
    client.sendall(local_file)
    print(colorama.Fore.RED+'Transfer has been completed')

def user_interface(client):
    while True:
        try:
            command=client.recv(1).decode('utf-8')
            print(command)
            if command == 'u':
                client.sendall('u - Command accepted , initiate upload'.encode('utf-8'))
                download(client)

            elif command == 'd':
                client.sendall('d - Command accepted , initiate download'.encode('utf-8'))
                upload(client)

            elif command == 'l':
                client.sendall('l - Command accepted , listing directory'.encode('utf-8'))
                client.sendall(db_list())

            elif command == 'e':
                client.sendall('e - closing session'.encode('utf-8'))
                client.close()
                break

            elif command ==  'h':
                client.sendall('h - Command accepted , initiate help'.encode('utf-8'))
                helpmesir(client)

            else:
                client.sendall('Invalid request , try again'.encode('utf-8'))
                continue
        except ConnectionError:
            client.close()
            break



#service initiation
print(colorama.Fore.YELLOW+'Initiating Service start up')
srv = Service()
srv.database()
while True:
    print(colorama.Fore.GREEN+'Waiting for connection')
    client , addr = srv.sock.accept()
    print(colorama.Fore.GREEN+f'Connection from address {addr} has been ESTABLISHED')
    user_interface(client)
