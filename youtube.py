import requests
import json
import sys
import os
import re
import urllib.request

#AIzaSyD70NZyqjSVx0HsCoGm-3MTG5GiwA4hWJk
#api key


def get_info(id):

	#url = 'https://www.youtube.com/watch?v=IL7VyRMbwwA'
	
	key = 'AIzaSyD70NZyqjSVx0HsCoGm-3MTG5GiwA4hWJk'
	#id = 'IL7VyRMbwwA'
	url = ('https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=snippet' % (id, key))
	#url = ('https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=contentDetails' % (id, key))

	session = requests.Session()
	response = requests.get(url,headers={'Accept': 'application/json'})
	x = response.json()
	s = 'linked: "'
	s+= x['items'][0]['snippet']['title']
	s+= '" by '
	s+= x['items'][0]['snippet']['channelTitle']
	return s
	#url2 = 'https://api.twitch.tv/kraken/channels/'+str(id)+'/'
	
	
def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None