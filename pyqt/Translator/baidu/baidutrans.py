#!/usr/bin/env python
# -*- coding: utf-8 -*- 


# test pass in environment with 'utf-8'
#	https://docs.python.org/2.4/lib/standard-encodings.html

import httplib
import md5
import urllib
import random
import config

DFL_ID = config.APPID
DFL_KEY = config.SECRET 

DFL_SRC = 'en'
DFL_DST = 'it'
DFL_API = 'api.fanyi.baidu.com'
DFL_URL = '/api/trans/vip/translate'

# http://api.fanyi.baidu.com/api/trans/product/apidoc
LANG_SUPPORT = {"zh", "en", "yue", "wyw", "jp", "kor", "fra", "spa", "th", "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est", "dan", "fin", "cs", "rom", "slo", "swe", "hu", "cht"}
ERRORMSG = { 
	52000: 'success', 
	52001: 'request timeout(pls retry)',
	52002: 'system error(pls retry)',  
	52003: 'unauthenticated(pls check your appid)',
	54000: 'not enough parameters',
	54001: 'signature error',
	54003: 'limited access frequency',
	54004: 'not adequate account fee(pay for it)',
	54005: 'frequent query request',
	58000: 'ip illegal',
	58001: 'language not support yet'
}

class baiduTranslator():
	def __init__(self, appid = DFL_ID, secretkey = DFL_KEY):
		self.appid = appid
		self.secretkey = secretkey
		self.client = httplib.HTTPConnection(DFL_API)
		self.raw = DFL_URL + '?appid=' + appid + '&q=%s' + '&from=%s&to=%s&salt=%s&sign=%s'
	
	def translate(self, text = None, src = DFL_SRC, dst = DFL_DST):
		if not text:
			return '' 
		if src == dst:
			return text
		try:
			url = self.regeneraterequest(text, src, dst)
			self.client.request('GET', url)
			res = self.client.getresponse().read()
			err = geterror(res)
			if err:
				return err
			return self.simpleresponse(res, dst)
		except Exception, e:
			print e
		finally:
			if self.client:
				self.client.close()
	
	def regeneraterequest(self, text, src, dst):
		salt = random.randint(32768, 65536)
		sign = self.appid + text + str(salt) + self.secretkey
		return self.raw%(text, src, dst, str(salt), md5.new(sign).hexdigest())

	def simpleresponse(self, response, dst):
		if response:
			s_index = response.find('"dst"') 
			if s_index < 0:
				return ''
			e_index = response[s_index+7:].find('"}')
			if e_index < 0:
				return ''
			res = response[s_index+7:][:e_index]
			if dst in LANG_SUPPORT:
				# for i in range(0x3040, 0x30a0): 
				#     print(unichr(i))
				# print u'{0}'.format(res), can be assigned
				# roughly decoding, maybe cause some problems
				res = res.decode('unicode-escape')
			return res
		return ''

def geterror(response):
	err_ind = response.find('"error_code"')
	if not err_ind < 0: 
		errno = int(response[err_ind+14:err_ind+19])
		if errno in ERRORMSG.keys():
			return ERRORMSG[errno]	
		else:
			return 'unknown error'
	return None 
	
