#!/usr/bin/env python
# coding: utf-8
import requests

def getToken():
	token_server = "https://openapi.baidu.com/oauth/2.0/token"
	data = {
		'grant_type'    : 'client_credentials',
		'client_secret' : 'VYsRsWM664GCwiAgeIguEYqijZc0a4Uq',
		'client_id'     : '7B7bycYz2ArgkNm1VpDgldj3'
	}
	tokenRes = requests.post(token_server, data=data).json()
	token = tokenRes['access_token']
	return token