#!/usr/bin/env python
# coding: utf-8
import requests
import tok

def translate(msg):

	token = tok.getToken()
	voice_server = "http://tsn.baidu.com/text2audio"
	dt = {
		'tex'  : msg,
		'lan'  : 'zh',
		'tok'  : token,
		'ctp'  : 1,
		'cuid' : 'vincentlou',
		'per'  : 3
	}

	voiceRes = requests.post(voice_server,data=dt,stream=True)
	voice_fp = open('./voice_gen_data/res.mp3','wb')
	voice_fp.write(voiceRes.raw.read())
	voice_fp.close()
