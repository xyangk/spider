# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 21:13:06 2015

@author: xiao
"""

import urllib
import urllib2
import re
'''
page = 1
url = 'http://www.qiushibaike.com/hot/page/'+str(page)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {"User-Agent":user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    #print reponse.read()
except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    if hasattr(e, 'reason'):
        print e.reason
content = response.read().decode('utf-8')


pattern = re.compile(r'<div.*?class="author">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div'+
r'.*?class="content">(.*?)<!--(.*?)-->.*?</div>(.*?)'+
r'<div class="stats".*?<i.*?class="number">(.*?)</i>', re.S)

items = re.findall(pattern, content)
for item in items:
    haveimg = re.search('img', item[3])
    if not haveimg:
        print item[0],item[2],item[1],item[4]
''' 

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []#存放段子的变量，每个元素是每一页的段子
        self.enable = False
        
    def getPage(self):
        try:
            url = 'http://www.qiushibaike.com/hot/page/'+str(self.pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'reason'):
                print u'连接失败，错误原因：',e.reason
            return None
    
    def getPageItems(self):
        pageCode = self.getPage()
        if not pageCode:
            print u'页面加载失败...'
            return None
        pattern = re.compile(r'<div.*?class="author">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div'+
                r'.*?class="content">(.*?)<!--(.*?)-->.*?</div>(.*?)'+
                r'<div class="stats".*?<i.*?class="number">(.*?)</i>', re.S)
        pageStories = []
        items = re.findall(pattern, pageCode)
        for item in items:
            haveimg = re.search('img', item[3])
            if not haveimg:
            	havebr = re.search('<br>|<br/>', item[1])
                replacebr = re.compile(r'<br>|<br/>')
                #x = item[1]
                if havebr:
                    x = re.sub(replacebr, '\n', item[1])#将换行符替换为\n
                    pageStories.append([item[0], item[2], x, item[4]])
                else:
                    pageStories.append([item[0], item[2], item[1], item[4]])
        return pageStories
    
    #预先加载
    def loadPage(self):
        #如果当前未看的页数小于2，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems()
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
                    
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return 
            print u'第%d页\t发布人:%s\t发布时间:%s\n%s\n赞:%s\n' %(page, 
                story[0],story[1], story[2], story[3])
                
    def start(self):
        print u'正在读取糗事百科，按回车查看新段子，Q退出'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()