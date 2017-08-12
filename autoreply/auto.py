#!/usr/bin/python
import itchat
import requests
import VtoT
import TtoV
import os
import re
import jieba
from wordcloud import WordCloud
import PIL.Image as Image
import numpy as np
from itchat.content import TEXT,RECORDING
itchat.auto_login(hotReload=True)


def getResponseFromRobot(msg):
	KEY = "354b2e3febca42a0b469f6b8a2f1f183"
	apiUrl = "http://www.tuling123.com/openapi/api"
	data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : "121202"
    }

	try:
		res = requests.post(apiUrl, data=data).json()
		return res.get('text')
	except:
		return None

hanhan = itchat.search_friends(name='hanhan')[0]['UserName']
me = itchat.search_friends(name='Vincent Lou')[0]['UserName']

STOP = 0

@itchat.msg_register(TEXT)
def text_reply(msg):
	global STOP
	'''CONTROL'''
	if msg['ToUserName']=='filehelper':
		if(msg['Text']=='pause'):
			STOP = 1
			itchat.send_msg('paused','filehelper')

		if(msg['Text']=='resume'):
			STOP = 0
			itchat.send_msg('resumed','filehelper')
			return

		if(msg['Text']=='gender'):
			friends = itchat.get_friends(update=True)
			male = female = other = 0
			for friend in friends:
				print(friend)
				sex = friend['Sex']
				if sex==1: male+=1
				elif sex==2: female+=1
				else: other+=1
			itchat.send_msg('male: %.2f' %(float(male)/len(friends)*100)+'%\n'+\
				'female: %.2f' %(float(female)/len(friends)*100)+'%\n'+\
				'other: %.2f' %(float(other)/len(friends)*100)+'%\n','filehelper')
			return
		if(msg['Text']=='cloud'):
			slist = []
			friends = itchat.get_friends(update=True)
			for friend in friends:
				sig = friend['Signature']

				emoji = re.compile('<span.*?</span>')
				none = re.compile('\s{2,}')

				sig = emoji.sub("",sig)
				sig = none.sub("",sig)
				if len(sig)>0:
					slist.append(sig)

			text = "".join(slist)

			wordList = jieba.cut(text, cut_all=True)
			ws = " ".join(wordList)

			coloring = np.array(Image.open("./wechat.jpg"))


			my_wordcloud = WordCloud(background_color="white", max_words=2000,
			                         mask=coloring, max_font_size=60, random_state=42, scale=2,
			                         font_path="C:\Windows\Fonts\msyhl.ttc").generate(ws)


			file_name_p = 'cloud.jpg'

			my_wordcloud.to_file(file_name_p)
			itchat.send('@img@%s' % file_name_p,'filehelper')
			os.remove(file_name_p)
			return


		

	# if (msg['FromUserName'] != hanhan and msg['ToUserName']!='filehelper') or STOP==1:
	# 	return

	fromUser = itchat.search_friends(userName=msg['FromUserName'])['NickName']
	print(fromUser+': '+msg['Text']+'\n')
	robot = getResponseFromRobot(msg['Text'])
	print('\t\t\t\treply: '+robot+'\n')
	return robot or "你说什么?"


@itchat.msg_register(RECORDING)
def voice_reply(msg):
	# if (msg['FromUserName'] != hanhan and msg['ToUserName']!='filehelper') or STOP==1:
	# 	return

	fromUser = itchat.search_friends(userName=msg['FromUserName'])['NickName']
	filename = msg['FileName'].split(".")[0]
	filepath = './voice_data/'+filename
	'''download'''
	msg['Text'](filepath+'.mp3')
	'''download'''
	res = VtoT.translate(filepath)
	os.remove(filepath+'.wav')
	print(fromUser+': '+res+'\n')
	
	default = '我听不清你在说什么'

	if(res=='ERROR'):
		return default
	else:
		robot = getResponseFromRobot(res)
		print('\t\t\t\treply: '+robot+'\n')
		TtoV.translate(robot)
		itchat.send_file('./voice_gen_data/res.mp3',msg['FromUserName'])
		os.remove('./voice_gen_data/res.mp3')

itchat.run()