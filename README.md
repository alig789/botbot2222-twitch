# botbot2222-twitch
Basic chatbot for twitch chat with a few main features:
- Logs messages for channels by default in botbot/botlogs
- References Universal quote list across channels/discord
- Provides information for Youtube video links posted in chat
- Pulls most recent tweet given a Twitter username
- Pulls stream name/current game
- Custom command list per channel
- Several basic fun commands

Main Commands:
- !quote [number]:
	 + Pulls quote from quotesinfo.txt with the given number and sends it to the chat. If left blank, a random quote is selected.
- !addquote [message]:
	 + Saves given message to quotesinfo.txt and repeats quote back with quote number. Must be a moderator to use this command.
- !delquote [number]:
	 + Deletes quote from quotesinfo.txt with the given quote number. Deleted quotes are saved in modified.txt. Must be a moderator to use this command.
- !addcmd [keyword message]:
	 + Adds a custom command only usable in the current channel. Keyword and message must be separated by a space. Overwrites commands with same name. Must be a moderator to use this command.
- !delcmd [keyword]:
	 + Deletes command with given keyword. Must be a moderator to use this command.
- !commands:
	 + Lists custom commands for current channel.
