#-*-coding:utf-8-*-
import urllib
import urllib2
import re

class Tool:
	#去除img标签，7位长空格
	removeImg = re.compile(r'<img.*?>| {7}')
	#删除超链接标签
	removeAddr = re.compile(r'<a.*?>|</a>')
	#把换行的标签换位\n
	replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
	#将表格制表符<td>换为\t
	replaceTD = re.compile(r'<td>')
	#将段落开头替换为\n加两个空格
	replacePara = re.compile(r'<p.*?>')
	#将换行符或双换行符替换为\n
	replaceBR = re.compile(r'<br><br>|<br>')
	#删除其余标签
	removeExtraTag = re.compile(r'<.*?>')
	def replace(self, x):
		x = re.sub(self.removeImg, '', x)
		x = re.sub(self.removeAddr, '', x)
		x = re.sub(self.replaceLine, '\n', x)
		x = re.sub(self.replaceTD, '\t', x)
		x = re.sub(self.replacePara, '\n  ', x)
		x = re.sub(self.replaceBR, '\n', x)
		x = re.sub(self.removeExtraTag, '', x)
		#strip()将删除前后多余的元素
		return x.strip()

class BDTB:
	def __init__(self, baseurl, seelz,floorTag):
		self.baseurl = baseurl
		self.seelz = '?see_lz='+str(seelz)
		self.tool = Tool()
		#全局file变量，文件写入操作对象
		self.file = None
		#楼层标号，初始为1
		self.floor = 1
		#默认标题
		self.defaultTitle = u'百度贴吧'
		#是否写入楼层分隔符
		self.floorTag = floorTag

	def getPage(self, pagenum):
		try:
			url = self.baseurl+self.seelz + '&pn='+str(pagenum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			#print response.read()
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print '链接失败，错误原因：',e.reason
				return None

	def getTitle(self, page):
		#page = self.getPage(1)
		pattern = re.compile(r'<h3.*?class="core_title_txt.*?>(.*?)</h3>')
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getPageNum(self, page):
		#page = self.getPage(1)
		pattern = re.compile(r'<li.*?class="l_reply_num".*?class="red">(.*?)</span>', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return 0

	def getContent(self, page):
		#page = self.getPage(1)
		pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
		result = re.findall(pattern, page)
		contents = []
		for item in result:
			content = '\n'+self.tool.replace(item)+'\n'
			contents.append(content.encode('utf-8'))
		return contents
		#print floor, u'楼----------------------------------------------\n'
		#print self.tool.replace(result[1])

	def setFileTitle(self, title):
		if title is not None:
			self.file = open(title+".txt","w+")
		else:
			self.file = open(self.defaultTitle+".txt","w+")

	def writeData(self, contents):
		for item in contents:
			if self.floorTag == '1':
				floorline = '\n'+str(self.floor)+u'-----------------------------\n'
				self.file.write(floorline)
			self.file.write(item)
			self.floor += 1

	def start(self):
		page = self.getPage(1)
		pagenum = self.getPageNum(page)
		title = self.getTitle(page)
		self.setFileTitle(title)
		if pagenum == None:
			print 'URL已失效，请重试'
			return 
		try:
			print "该帖子有"+str(pagenum)+"页"
			for i in range(1, int(pagenum)+1):
				print "正在写入第"+str(i)+'页'
				pagecontent = self.getPage(i)
				contents = self.getContent(pagecontent)
				self.writeData(contents)
		except IOError, e:
			print '写入异常，原因'+e.message
		finally:
			print '写入完成'

baseurl = 'http://tieba.baidu.com/p/'
print u'请输入帖子代号（默认3138733512）'
input = str(raw_input(u'http://tieba.baidu.com/p/'))
if input:
	url = baseurl + input
else:
	url = 'http://tieba.baidu.com/p/3138733512'
seelz = raw_input('是否只获取楼主发言？是1，否0\n')
floorTag = raw_input('是否划分楼层？是1，否0\n')
bdtb = BDTB(url, seelz, floorTag)
#bdtb.getTitle()
#bdtb.getPageNum()
bdtb.start()