from bs4 import BeautifulSoup
import urllib.request
import re


def read_webpage(link):
	r = urllib.request.urlopen(link)
	soup = BeautifulSoup(r.read().decode('ascii', 'ignore'),'html.parser')

	#story = soup.get_all('p')
	#print(type(soup.body))
	s = str(soup.find(id="storytextp"))
	
	#print(type(story))

	s = re.sub(r'<.+?>', '', s)
	s = s[0:4000]


	return(s)