import requests
import json
import sys
import os
import re
import urllib.request



def change_title(channel,title):

	url = 'https://api.twitch.tv/kraken/channels/'+channel

	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	id = response.json()['_id']
	url2 = 'https://api.twitch.tv/kraken/channels/'+str(id)+'/'
	#response = session.get(url2,headers={'Accept': 'application/vnd.twitchtv.v5+json'})
	#return response
	
	auth = load_auth_key(channel)
	if auth == -1:
		return "I'm not authorized to change your title, ask airball to give you the authorization link."
	
	response = session.put(url2,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/vnd.twitchtv.v5+json','Authorization':'OAuth '+auth},
								json={"channel": {"status": title}}
								)
	
	if response.json()['status']!=401:
		return "Successfully changed title to "+response.json()['status']
	return "Couldn't change the title! panicBasket"
	
def get_json(channel):

	url = 'https://api.twitch.tv/kraken/channels/'+channel

	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	return response.json()
	
def get_live_message(channel):

	url = 'https://api.twitch.tv/kraken/streams/'+channel
	
	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	x = response.json()
	if x['stream'] == None:
		return
	s = "NOW LIVE: https://twitch.tv/"
	s+= channel
	s+= " playing "
	s+= x['stream']['channel']['game']
	s+= " > "
	s+= x['stream']['channel']['status']
	return s
	#return response.json()
	
def check_live(channel):

	url = 'https://api.twitch.tv/kraken/streams/'+channel

	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	if response.json()['stream'] == None:
		return False
	if response.json()['stream']['stream_type'] == 'live':
		return True
	
def change_game(channel,game):

	url = 'https://api.twitch.tv/kraken/channels/'+channel

	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	id = response.json()['_id']
	url2 = 'https://api.twitch.tv/kraken/channels/'+str(id)+'/'
	#response = session.get(url2,headers={'Accept': 'application/vnd.twitchtv.v5+json'})
	#return response
	
	auth = load_auth_key(channel)
	if auth == -1:
		return "I'm not authorized to change your game, ask airball for the authorization link."
		
	response = session.put(url2,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/vnd.twitchtv.v5+json','Authorization':'OAuth '+auth},
								json={"channel": {"game": game}}
								)
	if response.json()['status']!=401:
		return "Successfully changed game to "+response.json()['game']
	return "Couldn't change the game! panicBasket"
	
def get_title(channel):
	url = 'https://api.twitch.tv/kraken/channels/'+channel

	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	title = response.json()['status']

	return title
	
def get_game(channel):
	url = 'https://api.twitch.tv/kraken/channels/'+channel

	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/json'})
	title = response.json()['game']

	return title
#url2 = 'https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=8cjnc2hcvau0moy2ezquda8ey629tw&redirect_uri=http://localhost&scope=channel_editor'
	#req = urllib.request.Request(url)
	#req.add_header("Client-ID","8cjnc2hcvau0moy2ezquda8ey629tw")
	#resp = urllib.request.urlopen(req)
	#return resp
	#data = resp.read()
	#return data
	
#silver = http://localhost/#access_token=rwky42aoea90r8lw50siwx5plqgdbm&scope=channel_editor
	
#botbot = http://localhost/#access_token=w1t02pefofpc11sf2s0i6lpi552f2l&scope=channel_editor	
	
def load_auth_key(channel):
	f = open('botbot/auth_keys.csv','r')
	xs = f.readlines()
	
	for i in xs:
		#print(i.split('"',2)[1].lower())
		if channel.lower() == i.split('"',2)[1]:
			return i.split('"',4)[3]

	return -1
	
def refresh_token():
	url = 'https://api.twitch.tv/kraken/oauth2/token/?grant_type=refresh_token&refresh_token=5wg5cxr9j6x9zwfok49zpg605lyhij&client_id=8cjnc2hcvau0moy2ezquda8ey629tw&client_secret=10j0zd3og43ndtelsc0hxpd0khwr6n'
	session = requests.Session()
	response = requests.get(url,headers={"Client-ID":"8cjnc2hcvau0moy2ezquda8ey629tw",'Accept': 'application/vnd.twitchtv.v5+json'})
	return response.json()
	
	#https://api.twitch.tv/kraken/oauth2/authorize?client_id=8cjnc2hcvau0moy2ezquda8ey629tw&redirect_uri=http://localhost&response_type=id_token&scope=openid