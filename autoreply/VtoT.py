#!/usr/bin/env python
# coding: utf-8
import requests
import json
import base64
import os
import tok
from pydub import AudioSegment

def translate(filename):
	sound = AudioSegment.from_mp3(filename+'.mp3')
	sound.export(filename+".wav", format="wav")


	token = tok.getToken()

	VOICE_RATE = 8000
	WAVE_FILE = filename+".wav"
	CUID = "vincentlou"
	WAVE_TYPE = "wav"


	f = open(WAVE_FILE,'rb')
	wave_file = f.read()
	speech = base64.b64encode(wave_file).decode('utf-8')
	update = {
		"format":WAVE_TYPE, 
		"rate":VOICE_RATE, 
		'channel':1,
		'cuid':CUID,
		'token':token,
		'speech': speech,
		'len':len(wave_file)}
	post_data = json.dumps(update)
	os.remove(filename+'.mp3')
	url = "http://vop.baidu.com/server_api"
	headers = { 'Content-Type' : 'application/json' } 
	res =  requests.post(url, data=bytes(post_data,encoding='utf-8'), headers=headers).json()
	if res['err_no']!=0:
		print(res)
		return 'ERROR'
	return res['result'][0]
	
