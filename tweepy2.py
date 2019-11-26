import tweepy #https://github.com/tweepy/tweepy
import re



#Twitter API credentials
consumer_key = "4eTO9CRjgO7NYgMULjgi6VRBh"
consumer_secret = "RJaAC0I6jD2erc7GDwp3YdeOSbd1JLrANHM62AseJn3ZSyW7RL"
access_key = "889870964573560832-m5QfqruWVHxaVRAaLXQMwo55WYSeGN3"
access_secret = "aHFeY3El2AGeY25wq5OfK5FS3k25ONG9rxRG0R79dohzX"


def get_all_tweets(screen_name='gabgab22222'):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=1)
	
	alltweets.extend(new_tweets)
	
	text = str((alltweets[0].text.encode('utf-8')))
	
	text = text[2:]
	text = text[:-1]
	
	username = str(alltweets[0].user.name)
	s = ""
	s+= username
	s+= " on Twitter: "
	s+= text
	
	return s
	
def send_tweet(text):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	try:
	#authorize twitter, initialize tweepy
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_secret)
		api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
		api.update_status(text)
	
		return "Successfully tweeted: "+text+""
	except:
		return "Something went wrong lol"
	
	# oldest = alltweets[-1].id - 1	
	# while len(new_tweets) > 0:
		# print("getting tweets before %s" % (oldest))
		
		# #all subsiquent requests use the max_id param to prevent duplicates
		# new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		# #save most recent tweets
		# alltweets.extend(new_tweets)
		
		# #update the id of the oldest tweet less one
		# oldest = alltweets[-1].id - 1
		
		# print( "...%s tweets downloaded so far" % (len(alltweets)))