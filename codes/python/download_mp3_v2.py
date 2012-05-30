#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################
#百度中批量下载某歌手的歌
###############################
import re,urllib,os
def down_one_mp3(author_name,song_name,filepath="F:/downloadmusic/"):
        if not os.path.exists(filepath):
                os.mkdir(filepath)
        song_url = "http://box.zhangmen.baidu.com/x?op=12&count=1&mtype=1&title="
        song_url=song_url+urllib.quote(song_name.encode('gbk'))
        song_url=song_url+'$$'+urllib.quote(author_name.encode('gbk'))+'$$$$&url=&listenreelect=0&.r=0.1696378872729838'
        #print(song_url)
        xmlfile=urllib.urlopen(song_url)
        xml_content=xmlfile.read()
        xml_content=xml_content.decode('gbk')
        url1 = re.findall('<encode>.*?CDATA\[(.*?)\]].*?</encode>',xml_content)
        url2 = re.findall('<decode>.*?CDATA\[(.*?)\]].*?</decode>',xml_content)
        url=url1[0][:url1[0].rindex('/')+1] + url2[0]
        print(author_name+' '+song_name)
        urllib.urlretrieve(url,filepath+song_name+'.mp3')
def download(author_name=u"陈奕迅",filepath="F:/downloadmusic/"):
        """
百度中批量下载某歌手的歌
url为陈奕迅的歌
filepath为保存的文件夹
"""
        
        url="http://mp3.baidu.com/songlist/"+urllib.quote(author_name.encode('gbk'))+".html"
        if not os.path.exists(filepath):
                os.mkdir(filepath)
        res=urllib.urlopen(url)
        content=res.read()
        res.close()
        content_gbk=content.decode('gbk')
        td=re.compile('\)">.*</a><div class="auth">')
        names=re.findall(td,content_gbk)
        i=0
        for name in names:
                try:
                        song_name=name[3:-22]
                        print(song_name)
                        song_url = "http://box.zhangmen.baidu.com/x?op=12&count=1&mtype=1&title="
                        song_url=song_url+urllib.quote(song_name.encode('gbk'))
                        song_url=song_url+'$$'+urllib.quote(author_name.encode('gbk'))+'$$$$&url=&listenreelect=0&.r=0.1696378872729838'
                        #print(song_url)
                        xmlfile=urllib.urlopen(song_url)
                        xml_content=xmlfile.read()
                        xml_content=xml_content.decode('gbk')
                        url1 = re.findall('<encode>.*?CDATA\[(.*?)\]].*?</encode>',xml_content)
                        url2 = re.findall('<decode>.*?CDATA\[(.*?)\]].*?</decode>',xml_content)
                        url=url1[0][:url1[0].rindex('/')+1] + url2[0]
                        urllib.urlretrieve(url,filepath+song_name+'.mp3')
                except:
                        pass
if __name__=='__main__':
        #download()
        down_one_mp3(author_name=u"陈奕迅",song_name=u"十年")
        os.system("pause")
