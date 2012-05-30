#!/usr/bin/env python
# -*- coding: utf-8 -*-
from VideoCapture import Device
import sys,pygame,socket,time,threading
def cmd_input(remote_host='10.21.48.142',port=50011):
    myhelp="'q' or 'start' or 'stop'"
    while True:
        cmd=raw_input('command: ')
        if cmd=='q':
            cmd_socket('quit',remote_host,port)
            break
        elif cmd=='start':
            cmd_socket('start',remote_host,port)
        elif cmd=='stop':
            cmd_socket('stop',remote_host,port)
        else:
            print(myhelp)
            
def cmd_socket(cmd,host,port):
    global capture_flag
    bufsize=1024
    cmd_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cmd_sock.connect((host,port))
    cmd_sock.send(cmd)
    data=cmd_sock.recv(bufsize)
    cmd_sock.close()
    if cmd=='start':
        capture_flag=True
        video=capture_socket(port+1,port,host)
        video.start()
    elif cmd=='stop':
        capture_flag=False
    elif cmd=='quit':
        capture_flag=False
        #if capture_flag:
        sys.exit()
    else:
        print(data)
class capture_socket(threading.Thread):
    def __init__(self,capture_port,cmd_port,remote_host):
        super(capture_socket,self).__init__()
        self.capture_port=capture_port
        self.cmd_port=cmd_port
        self.remote_host=remote_host
    def run(self):
        global capture_flag
        quit_flag=False
        bufsize=100000
        host=socket.gethostbyname(socket.gethostname())
        #print(host,self.capture_port)
        capture_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        capture_sock.bind((host,self.capture_port))
        pygame.init()
        res=(160,120)
        screen=pygame.display.set_mode(res)
        pygame.display.set_caption('justin')
        while capture_flag:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    cmd_socket('stop',self.remote_host,self.cmd_port)
                    quit_flag=True
                    pygame.quit()
                    break
            if quit_flag:
                break
            data,addr=capture_sock.recvfrom(bufsize)
            if data=='cap':
                pygame.quit()
                break
            camshot=pygame.image.frombuffer(data,res,"RGB")
            screen.blit(camshot,(0,0))
            pygame.display.flip()
        capture_sock.close()
        #capture_flag=True
if __name__=='__main__':
    capture_flag=True
    cmd_input()
