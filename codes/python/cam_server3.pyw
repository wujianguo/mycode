#!/usr/bin/env python
# -*- coding: utf-8 -*-
from VideoCapture import Device
import pygame,socket,Image,time,threading
def cmd_recv(port=50011):
    global capture_flag
    bufsize=1024
    cmd_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host=socket.gethostbyname(socket.gethostname())
    cmd_sock.bind((host,port))
    cmd_sock.listen(1)
    while True:
        new_cmd_sock,remote_addr=cmd_sock.accept()
        data=new_cmd_sock.recv(bufsize)
        new_cmd_sock.send(data)
        new_cmd_sock.close()
        if data=='quit':
            capture_flag=False
        elif data=='start':
            capture_flag=True
            video=capture_socket(port+1,remote_addr[0])
            video.start()
        elif data=='stop':
            capture_flag=False
        else:
            pass

class capture_socket(threading.Thread):
    def __init__(self,capture_port,remote_host):
        super(capture_socket,self).__init__()
        self.remote_host=remote_host
        self.capture_port=capture_port
    def run(self):
        global capture_flag
        capture_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        pygame.init()
        cam=Device()
        cam.setResolution(160,120)
        while capture_flag:
            camshot=cam.getImage()
            #camshot=camshot.tostring()
            capture_sock.sendto(camshot.tostring(),(self.remote_host,self.capture_port))
            #print("send ok")
            time.sleep(0.1)
        del cam
        capture_sock.sendto("cap",(self.remote_host,self.capture_port))
        capture_sock.close()
if __name__=='__main__':
    capture_flag=True
    cmd_recv()
