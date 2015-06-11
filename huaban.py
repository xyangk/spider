#-*-coding:utf-8-*-
import requests
import re
import os

class Huaban():
	def __init__(self, cat = 'beauty'):
		self.homeurl = 'http://huaban.com/favorite/'+cat +'/'
		self.images = []
		if not os.path.exists(cat):
			os.mkdir(cat)
		self.dir = cat

	def __load_homePage(self):
		#加载主页面
		return requests.get(url = self.homeurl).content

	def __make_ajax_url(self, No):
		#返回ajax请求的url
		return self.homeurl+'?iaqkmzos&max='+No+'&limit=20&wfl=1'

	def __load_more(self,id):
		return requests.get(url=self.__make_ajax_url(id)).content

	def __process_data(self, htmlPage):
		prog = re.compile(r'app.page\["pins"\].*')
		appPins = prog.findall(htmlPage)
		null = None
		true = True
		if appPins == []:
			return None
		result = eval(appPins[0][19:-1])
		#print result
		#for i in result:
		#	print i['user']['username'].decode('utf-8')
		for i in result:
			info = {}
			info['id'] = str(i['pin_id'])
			info['url'] = 'http://img.hb.aicdn.com/'+str(i['file']['key'])+'_fw658'
			if i['file']['type'][:5] == 'image':
				info['type'] = i['file']['type'][6:]#图片格式
			else:
				info['type'] = 'NoName'
			self.images.append(info)

	def __save_image(self, picname, content):
		#for pic in images:
			#req = requests.get(pic['url'])
			#picname = pic['id']+'.'+pic['type']
		with open(picname, 'wb') as fp:
			fp.write(content)

	def get_image_info(self, num=1):
		self.__process_data(self.__load_homePage())
		for i in range(num-1):
		    self.__process_data(self.__load_more(self.images[-1]['id']))
		    #pass
		return self.images

	def downloadimg(self):
		print "{} images will be download".format(len(self.images))
		for key, pic in enumerate(self.images):
			#print 'Download {}...'.format(key+1)
			print u'正在下载第%3d张...' % (key+1)
			try:
				req = requests.get(pic['url']).content
				#pass
			except:
				print 'error'
			picname = os.path.join(self.dir,pic['id']+'.'+pic['type'])
			self.__save_image(picname, req)

if __name__=='__main__':
	print u"输入分类(如:beauty),默认:http://huaban.com/favorite/beauty/"
	category = raw_input()
	if category:
		hb = Huaban(category)
	else:
		hb = Huaban()
	print u'每次下载20张，下载几次？默认一次'
	num = raw_input()
	if num:
		hb.get_image_info(int(num))
	else:
		hb.get_image_info(1)
	hb.downloadimg()
