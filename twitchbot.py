import socket
import discord
import random
import time
import urllib.request

import bs42
import tweepy2
import re
import stages
import emoji
import datetime

import stream
import youtube


while (1==1):
	try:
		HOST = "irc.twitch.tv"
		PORT = 6667
		NICK = "botbot2222"
		PASS = 'oauth:z4hkfdl6fd18dloput20zkroktg9z3'
		globaltime = 0
		delay_dict = {}
		command_list = {}

		def is_mod(line):
			if "badges=" in line and "display-name=" in line and 'subscriber=' in line and 'mod=1' in line or is_broadcaster(line):
				return True
			else:
				return False
				
		def is_broadcaster(line):
			if "badges=broadcaster" in line and "display-name=" in line and 'subscriber=' in line:
				return True
			else:
				return False

		def send_message(message,channel,delay=2):
			global delay_dict
			#print(time.time() - delay_dict.get(channel))
			#print(delay_dict)
			if time.time() - delay_dict.get(channel) < 0:
				return
			s.send(bytes("PRIVMSG #" + channel + " :" + message + "\r\n", "UTF-8"))
			delay_dict[channel] = time.time() + delay
			log('botbot2222', message, channel)
			
		def send_no_delay(message,channel):
			s.send(bytes("PRIVMSG #" + channel + " :" + message + "\r\n", "UTF-8"))
			
		def send_to_server(message):

			s.send(bytes(message + " :tmi.twitch.tv\r\n", "UTF-8"))

			
		def log(username, message, channel):
			time = str(datetime.datetime.now())
			f = open("botbot/botlogs/"+channel + ".txt",'a+')
			message2 = message.encode('utf-8', 'ignore')
			message3 = str(message2)[2:]
			message4 = message3[:-1]
			if message4 == "'":
				return
			try:
				f.write("(" + time + ") " +username +": "+ message4+ '\n')
				f.close()
			except RuntimeErrorError:
				print("FAILED")

		def connect_to_channels():
			global delay_dict
			
			f = open('botbot/botbotchannels.txt','r')
			channel_list = f.readlines()
			try:
				for i in channel_list:
					s.send(bytes("JOIN #"+i+" \r\n", "UTF-8"))
					channel_name = i[:-1]
					delay_dict[channel_name] = 0
					#print("joined #"+i)
			except:
				print('error joining #'+i)
			#print(delay_dict)
			
		def add_cmd(message,channel):
			global command_list
			command = message.split(" ",2)
			#print(command)
			string1 = ""
			string1+= '"'+command[1]+'","'+command[2]+'"\n'
			#print(s)
			try:
				fs = open('botbot/commands/'+channel+'.csv','r')
				xs = fs.readlines()

				exists = False
				for i in xs:
					if command[1].lower() == i.split('"',2)[1].lower():
						exists = True
						xs[xs.index(i)] = string1
						break
				if exists:
					f = open('botbot/commands/'+channel+'.csv','w+')
					f.writelines(xs)
					f.close()
					command_list[channel][command[1]] = command[2]
					msg = "Added command: "+command[1]
				
				else:
					f = open('botbot/commands/'+channel+'.csv','a+')
					f.write(string1)
					f.close()
					command_list[channel][command[1]] = command[2]
					msg = "Added command: "+command[1]
			except:
				f = open('botbot/commands/'+channel+'.csv','a+')
				f.write(string1)
				f.close()
				command_list[channel][command[1]] = command[2]
				msg = "Added command: "+command[1]
			return msg
			
		def del_cmd(message,channel):
			global command_list
			command = message.split(" ",1)
			#print(command)
			
			#print(s)
			try:
				fs = open('botbot/commands/'+channel+'.csv','r')
				xs = fs.readlines()

				exists = False
				for i in xs:
		#print(i.split('"',2)[1].lower())
					if command[1].lower() == i.split('"',2)[1].lower():
						exists = True
						
						xs.pop(xs.index(i))
						
						break
				if exists:
					f = open('botbot/commands/'+channel+'.csv','w+')
					f.writelines(xs)
					f.close()
					command_list[channel].pop(command[1])
					msg = ("Sucessfully deleted command: "+command[1])
				
				else:
					msg = "Couldn't find that command!"
			except:
				
				msg = "Couldn't find any commands to delete!"
			return msg
			
		def load_commands():
			global command_list
			
			f = open('botbot/botbotchannels.txt','r')
			channel_list = f.readlines()
			
			for i in channel_list:
				try:
					channel_name = i[:-1]
					command_list[channel_name] = {}
					
					fs = open('botbot/commands/'+channel_name+'.csv','r')
					xs = fs.readlines()
					#print(xs)
					for j in xs:
						key = j.split('"',2)[1]
						command = j.split('"',3)[3][:-2]
						command_list[channel_name][key] = command
				except:
					print('error adding commands: '+ i)

		s = socket.socket()
		s.connect((HOST, PORT))
		s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
		s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
		#s.send(bytes("JOIN #botbot2222,#airball12,#coldeggman,#odmewhirter,#cool_nick__,#gabgab2222 \r\n", "UTF-8"))
		connect_to_channels()
		load_commands()
		s.send(bytes("CAP REQ :twitch.tv/membership \r\n", "UTF-8"))
		s.send(bytes("CAP REQ :twitch.tv/tags \r\n", "UTF-8"))
		s.send(bytes("CAP REQ :twitch.tv/commands \r\n", "UTF-8"))

		print('connected')


		while True:
			line = str(s.recv(1024))
			if "End of /NAMES list" in line:
				break

		while True:
			for line in str(s.recv(1024)).split('\\r\\n'):
				#print(line)
				if "PING" in line:
						#print("ping")
						send_to_server("PONG")
				parts = line.split(':',3)
				
				if "PRIVMSG" not in line:
					continue
				
				# if "jtv MODE" in line and "+o" in line:
					# mod = line.split("+o ")
					# mod = mod[1]
					# mod_channel = line.split("#")
					# mod_channel = mod_channel[1].split(" +o")
					# mod_channel = mod_channel[0]
					# print(">>>>>"+mod+"<<<< is mod in >>>>>" + mod_channel+ "<<<<<<")
					
				# if "jtv MODE" in line and "-o" in line:
					# mod = line.split("-o ")
					# mod = mod[1]
					# mod_channel = line.split("#")
					# mod_channel = mod_channel[1].split(" -o")
					# mod_channel = mod_channel[0]
					# print(">>>>>"+mod+"<<<< is no longer mod in >>>>>" + mod_channel+ "<<<<<<")

				
				
				if len(parts) < 3:
					continue
				
				
				if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
					#if ';user-id=' in line and 'emotes=;' not in line:
					#print('kappa in line')
					#print(parts)
					no_emotes_pls = line.split('user-type=',1)[1]
					parts1 = no_emotes_pls.split(':',2)
					#print(parts1)
					message = parts1[2]
					usernamesplit = parts1[1].split("!")
					channel = parts1[1].split("#")
					#else:
					#	print('wat')
						# parts1 = line.split(':',3)
						# message = parts1[2]
						# usernamesplit = parts1[1].split("!")
						# channel = parts1[1].split("#")

				#usernamesplit = parts[1].split("!")
				username = usernamesplit[0]
				
				
				# if username.startswith('tmi.twitch.tv'):
					# if "PRIVMSG" in line:
						# channel = parts[1].split("PRIVMSG")
					# else:
						# channel = "tmi.twitch.tv"
				#else:
				#channel = parts[1].split("#")
				
				try:
					channel = channel[1].lower()
					channel = channel[:-1]
				except IndexError:
					channel = "gixbot"
				
				#print(username)
				#print(message)
				#print(channel)
				
				if "PRIVMSG" in line:
					log(username, message, channel)
				
				
				custom_command = False
				
				for k in command_list[channel]:
					if message == k:
						msg =  command_list[channel][k]
						send_message(msg, channel)
						custom_command = True
						break
				if custom_command:
					continue
					
				if message.startswith("!addcmd "):
					if is_mod(line):
						try:
							msg = add_cmd(message, channel)
							send_message(msg,channel) 
						except:
							msg = "there was an error adding that command"
							send_message(msg,channel)
						continue
					else:
						msg = "You need to be a moderator to add commands!"
						send_message(msg,channel)
				
				if message.startswith("!delcmd "):
					if is_mod(line):
						try:
							msg = del_cmd(message, channel)
							send_message(msg,channel) 
						except:
							msg = "there was an error deleting"
							send_message(msg,channel)
						continue
					else:
						msg = "You need to be a moderator to remove commands!"
						send_message(msg,channel)
							
					
					
					
				if message.upper() == "OBJECTION":
					msg = "overruled"
					send_message(msg,channel)
					
				if message == "!com":
					print(command_list)
					#send_message(msg,channel)

				if message.startswith("!game "):
					if is_broadcaster(line):
						game = message.split(" ",1)[1]
						x = stream.change_game(channel,game)
						send_no_delay(x,channel)
						
				if message== "!game":
					x = str(stream.get_game(channel))
					send_message(x,channel)
				
				if message== "!title":
					x = str(stream.get_title(channel))
					send_message(x,channel)
						
				if message.startswith("!title "):
					if is_broadcaster(line):
						title = message.split(" ",1)[1]
						x = stream.change_title(channel,title)
						send_no_delay(x,channel)
				
				if message.find('youtube.com')>0:
					try:
						id = message.split('watch?v=',1)[1][:11]
						x = username
						x += " "
						x += (youtube.get_info(id))
						send_no_delay(x,channel)
					except:
						print('error')
						
				if message.find('youtu.be/')>0:
					try:
						id = message.split('youtu.be/',1)[1][:11]
						x = username
						x += " "
						x += (youtube.get_info(id))
						send_no_delay(x,channel)
					except:
						print('error')
					
					
				if message == "!swag":
					msg = "( ͡° ͜ʖ ͡°) swaggity swoogity comin in for dat booty ( ͡° ͜ʖ ͡°)"
					send_message(msg,channel)
					


					
				if message == "!gab":
					msg = "brb"
					send_message(msg,channel)

					
				if message == "I love you botbot2222":
					msg = "I love you too " + username + " <3 <3 <3"
					send_message(msg,channel)

					
				if message == "FrankerZ":
					msg = "FrankerZ = Dog Face (no space)"
					send_message(msg,channel)

					
					
				if message == "!me":
					msg = "You're " + username + " way to go buddy Kappa b"
					send_message(msg,channel)

					
					
				if message.upper() == "HELLO?":
					msg = "Is it me you're looking for?"
					send_message(msg,channel)
					
				if message == "!discord":
					if channel == 'coldeggman':
						msg = "Wanna talk with cold more closely? wanna play with him? you don't know how to come closer to him? you can join right now his new discord Coldeggman Keepos! you can know what is happening with steam situation or just talk with him normally its totally FREE! Join now!: https://discord.gg/nKsffjU"
					else:
						msg = "Join Gab's discord here: https://discord.gg/uECa4mN CatBag"
					send_message(msg,channel)
				
				if message == "!splatfest":
					msg = 'Check this link for splatfest stats: https://docs.google.com/spreadsheets/d/1PUfEawd6PtDPZVDNCMoFNmMjg6LiGPyiEUSetYm1SGw/edit?usp=sharing OpieZ'
					send_message(msg,channel)
					
				if message == "FoSho":
					msg = "IntoYou"
					send_message(msg,channel)

					
				if message == "IntoYou":
					msg = "FoSho"
					send_message(msg,channel)

					
				if message == "AllAboutYou":
					msg = "AllAboutYou"
					send_message(msg,channel)

					
				if message == "back":
					msg = "welcome back " + username + "!"
					send_message(msg,channel)

					
				if message == "!silver":
					msg = "neeeeeeeeerd MiniKeepo"
					send_message(msg,channel)

					
				if message == "JUSTDOIT":
					msg = "DONT LET YOUR MEMES BE DREAMS YESTERDAY YOU SAID TOMORROW SO JUST BLAZE IT #420"
					send_message(msg,channel)

					
				if message == "!cold":
					print(">>>"+channel+"<<<")
					msg = "PJSalt MiniKeepo"
					send_message(msg,channel)

					
				if message == "!commands":
					commandlist = "Custom commands for this channel:   "
					for k in command_list[channel]:
						commandlist+= k
						commandlist+=", "
					msg = commandlist[:-2]
					#msg = "View my outdated command list here: http://pastebin.com/WRdJSPQp CatBag"
					send_message(msg,channel)

					
				
					
				
					
				if message == "anyone here":
					msg = "no De3"
					send_message(msg,channel)

					
				if message == "!roll":
					rolls = list(range(1,7))
					actual_roll = str(random.choice(rolls))
					msg = "" + username + " rolls a " + actual_roll + "."
					
					send_message(msg,channel)

					
				if message == "!roIl":
					msg = "" + username + " rolls a 2222."
					
					send_message(msg,channel)

					
				if message.startswith('!8ball '):
					msg = username + ": " 
					fs = open('ball.txt', 'r')
					choices = fs.readlines()
					final_choice = random.choice(choices)
					fs.close()
					final_decision = (msg + final_choice)
					
					send_message(final_decision,channel)


				if message.startswith('!rw'):
				
					
					fs = open('weapons.txt', 'r')
					lines = fs.readlines()
					
					
					weapon = random.choice(lines)
					
					
					fs.close()
					

					send_message(weapon,channel)


					
				if message.startswith('!pickup '):
					pickupee = message[8:] 
					fs = open('pickup2.txt', 'r')
					pickup_lines = fs.readlines()
					actual_line = random.choice(pickup_lines)
					fs.close()
					final_pickup = ('Hey ' + pickupee + ', ' + actual_line)	
					send_message(final_pickup,channel)

					
				if message == "!gab":
					msg = "brb"
					send_message(msg,channel)

					
				if message == "!bandit":
					msg = "STAMP STAMP STAMP STAPMSTAAPMSSTPAMPSTAMPSTAMP SwiftRage"
					send_message(msg,channel)

					
				if message == "!info":
					msg = "I'm a twitch/discord bot made by airball12. If you want to add me to your channel, go to twitch.tv/botbot2222 and type !join in the chat! CatBag"
					send_message(msg,channel)

					
					
				if message == "!wr":
					msg = "Rhythm Heaven Fever All Medals: 1:52:35 by TehWhack, find more runs at http://www.speedrun.com/gabgab2222"
					send_message(msg,channel)

					
				if message == "!umbra":
					msg = "senpaibag"
					send_message(msg,channel)

					
				if message == "#stopthebotbotabuse":
					msg = "BibleThump http://i.imgur.com/a4aIuAP.png 1 like = 1 quote"
					send_message(msg,channel)

					
				if "9 plus 10" in message:
					msg = "21"
					send_message(msg,channel)

					
				if message == "NotLikeThis":
					msg = "how could this happen to me BibleThump"
					send_message(msg,channel)

					
				if "anime" in message.lower():
					msg = "/w "+username+" WEEEEEEEEB Kappa"
					send_no_delay(msg,channel)

					
				if message == "!dedede":
					msg = "De3 I ' L L   K I C K   T H A T   K I R B Y   T O   T H E   C U R B De3"
					send_message(msg,channel)
					
				

					
				if message == "!De3":
					if username == "airball12" or username == "gabgab2222":
						time.sleep(2)
						send_no_delay("De3 BADAPAP De3",channel)
						time.sleep(2)
						send_no_delay("De3 kirby, kirby kirby that's a name you should know De3",channel)
						time.sleep(2)
						send_no_delay("De3 kirby, kirby kirby he's the star of the show De3",channel)
						time.sleep(2)
						send_no_delay("De3 he's more than you think, he's got MAXIMUM PINK De3",channel)
						time.sleep(2)
						send_no_delay("De3 kirby, kibry kirby's the oneeee De3",channel)
						time.sleep(2)
						send_no_delay("De3 he comes riiiiiiiight back at ya De3",channel) 
						time.sleep(2)
						send_no_delay("De3 he comes riiiiiiiiiiight back at ya De3",channel) 
						time.sleep(2)
						send_no_delay("De3 give it all that you've got, take your very best shot, he'll send it right back at ya FoSho , YEAH De3",channel)
						time.sleep(2)
						send_no_delay("De3 How can I help you king dedede De3",channel)
						time.sleep(2)
						send_no_delay("De3 I need a monsta to clobba dat dair kirbee De3",channel)
						time.sleep(2)
						send_no_delay("De3 That's what we do best at NME De3",channel)
						time.sleep(2)
						send_no_delay("De3 You better get it with a money back GUARANTEE De3",channel)
						time.sleep(2)
						send_no_delay("De3 doooo dooo doooo dooo doo dodododododododo De3",channel)
						time.sleep(2)
						send_no_delay("De3 dooodly dooodly dooooooOOOOOOOOHHHHH De3",channel)
						time.sleep(2)
						send_no_delay("De3 kirby kirby kirbah, savin the day De3",channel)
						time.sleep(2)
						send_no_delay("De3 kirby kirby kirby he's here to stay De3",channel)
						time.sleep(2)
						send_no_delay("De3 Don't be fooled by his size, you won't believe your eyes De3",channel)
						time.sleep(2)
						send_no_delay("De3 KIRBY....kirbeh....KIRRRRBBBBAAAYYYYYY kirbeh De3",channel)
						time.sleep(2)
						send_no_delay("De3 kirby, kirby, kirby kirby kirby's the oooooooooooooooooooooooooonneeee. De3",channel)
						time.sleep(2)
						send_no_delay("De3 RIGHT BACK AT YA.....YEAH De3",channel)
						time.sleep(2)
						send_message("De3",channel,20)

					

					
					
				if message.startswith("!addquote "):
					if is_mod(line):
						quote_content = message
						quote_content = quote_content[10:]
						quote_content = quote_content.replace("\\","")
						fs = open('quotesinfo.txt', "a")
						fs.write(quote_content + "\n")
						fs.close()
						fs = open('quotesinfo.txt', "r")
						lines = fs.readlines()
						lines.insert(0,0)
						quote_num = len(lines)
						fs.close()
						msg = ("Added quote " +str(quote_num -1 )+": " + quote_content )
						send_message(msg, channel)

					else:
						msg = "You must be a moderator to add quotes!" 
						send_message(msg,channel)

				if message.startswith("!delquote "):
					if is_mod(line):
						try:
							quotenumber = int(message[10:])
							
							f = open('quotesinfo.txt','r')
							lines = f.readlines()
							deleted = lines[quotenumber-1]
							lines[quotenumber-1] = "\n"
							f.close()
							fs = open('modified.txt',"a")
							fs.write(""+ username + " removed quote "+str(quotenumber)+": "+deleted)
							fs.close()
							f = open('quotesinfo.txt','w')
							f.writelines(lines)
							f.close()
							msg = "Deleted quote "+str(quotenumber)+ ": "+deleted
							send_message(msg,channel)
						except:
							send_message("Couldn't delete that quote.",channel)
					else:
						send_message("You need to be mod to delete quotes!",channel)
						
					
				if message.startswith("!quote"):
					
					if message == '!quote':
						fs = open('quotesinfo.txt', "r")
						lines = fs.readlines()
						lines.insert(0,'"fix your bot"- everyone 2017')
						quote = random.choice(lines)
						fs.close()
						send_message(quote, channel)

					else:
						try:
							quote_number = int(message[7:])
							fs = open('quotesinfo.txt', "r")
							lines = fs.readlines()
							lines.insert(0,'"fix your bot"- everyone 2017')
							quote = lines[quote_number]
							fs.close()
							send_message(quote, channel)

						except:
							continue
							
					

					
				if message.startswith("!tweet"):
					
					if message == '!tweet':
						final_tweet = tweepy2.get_all_tweets()
						send_message(final_tweet, channel)

					
					else:
						final_tweet = tweepy2.get_all_tweets(message[7:])
						send_message(final_tweet, channel)


				# if message.startswith("!s2"):
					# x = stages.twitch_stage()
					# if message == "!s2":
						# send_no_delay(x[1],channel)
						# time.sleep(2)
						# send_message(x[2],channel)
						# time.sleep(2)

					# elif message == "!s2 next":
					
						# send_no_delay(x[3],channel)
						# time.sleep(2)
						# send_no_delay(x[4],channel)
						# time.sleep(2)
						# send_message(x[5],channel)

						
					# elif message == "!s2 later":
					
						# send_no_delay(x[6],channel)
						# time.sleep(2)
						# send_no_delay(x[7],channel)
						# time.sleep(2)
						# send_message(x[8],channel)

						
				if message == "!join":
					if username in delay_dict.keys():
						send_message("I'm already in your channel, "+username+"!",channel)

						continue
					if channel == 'botbot2222':
						try:
							fs = open('botbot/botbotchannels.txt', 'a')
							fs.write(""+username + "\n")
							fs.close()
							send_to_server("JOIN #"+username)
							delay_dict[username] = 0
							send_no_delay('/w airball12 '+username+' added me to their channel! PogChamp', channel)
					
							send_message("I joined your channel, "+username+"!",channel)

						except:
							send_message("there was an error joining your channel :/ try asking airball whats up", channel)

					
				if "BOTBOT" in message.upper():
					msg = "CatBag"
					send_message(msg,channel)
	except:
		continue
		
	
			
			

			
		