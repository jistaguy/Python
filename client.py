import socket
import sys
import colorama
import json
colorama.init(autoreset=True)

def connector():
    host=input('Enter IP address of the server ')
    port=31415
    print(colorama.Fore.GREEN+f'starting connection to {host} on port {port}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    print(colorama.Fore.GREEN+f'Connection to server {host} has been ESTABLISHED')
    return sock

class Header():
    def __init__(self,file_size=0,file_name=0,recv_data=0,send_data=0):
        self.file_size=file_size
        self.file_name=file_name
        self.recv_data=recv_data
        self.send_data=send_data

def convert_to_dict(obj):
    obj_dict={"__class__":obj.__class__.__name__}
    obj_dict.update(obj.__dict__)

    return obj_dict

def dict_to_obj(obj_dict):

    if "__class__" in obj_dict:
        class_name = obj_dict.pop('__class__')
    
    message_header = eval(class_name)(**obj_dict)
    
    return message_header
 
def file_preparation(direction):
    while True:
        try:
            if direction == 's':
                file_path=input('Enter complete path location of file location :')
            else:
                file_path=input('Enter complete path location to store recvied file :')
            file_path=file_path.replace('\\','/',-1)
            file_name=input('Enter file name including extension: ')
            break
        except:
            print(colorama.Fore.GREEN+'something wrong has been placed , try again')
    return file_path,file_name
  
def download(sock):
    #Send server the desired file to download
    file_info = file_preparation('r')
    sock.sendall(file_info[1].encode('utf-8'))

    #App header creation for the file
    message_header = sock.recv(135).decode('utf-8')
    message_header = json.loads(message_header)
    message_header = dict_to_obj(message_header)

    #data storage unit
    file_data = b''

    while message_header.file_size > message_header.recv_data:
        file_data += sock.recv(message_header.file_size)
        message_header.recv_data = len(file_data)
        percentage=int(message_header.recv_data/message_header.file_size*100)
        print(f'The following percentage of data has been transfered: {percentage}%')
    
    #save recivied file
    open(file_info[0]+file_info[1],mode='wb').write(file_data)
    print(colorama.Fore.RED+'Transfer has been completed')

def upload(sock):
    #file path execution
    file_info = file_preparation('s')
    
    #file openning
    local_file = open(file_info[0]+file_info[1],mode='rb').read()

    #Header creation and transfer preparation
    message_header = Header(sys.getsizeof(local_file),file_info[1])
    message_header = convert_to_dict(message_header)
    message_header = json.dumps(message_header).encode('utf-8')

    #Object transfer
    sock.sendall(message_header)

    #data file 
    sock.sendall(local_file)
    print(colorama.Fore.RED+'Transfer has been completed')
    

def user_interface(sock):
    while True:
        #get input from client send to server for validation
        print('To get command reference , please enter "h"')
        command=input('Enter command you want to initiate: ')
        sock.sendall(command.encode('utf-8'))

        #Server respond in order to understand how to act further
        respond=sock.recv(4096).decode('utf-8')
        print(colorama.Fore.GREEN+respond)

        #Check what to do base on server respond
        if respond[0] == 'u':
            upload(sock)

        elif respond[0] == 'd':
            download(sock)
            
        elif respond[0] == 'h':
            print(colorama.Fore.RED+sock.recv(4096).decode('utf-8'))
        
        elif respond[0] == 'l':
            print(colorama.Fore.RED+sock.recv(4096).decode('utf-8'))
        
        elif respond[0] == 'e':
            sock.close()
            print(colorama.Fore.RED+'Closing client')
            sys.exit()
        
        #in case of typo just try again
        else:
            continue

while True:
    #connection ESTABLISHMENT
    sock=connector()
    #User interface for control over app
    user_interface(sock)

