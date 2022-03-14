import discord, json, threading
from datetime import datetime, timedelta
from time import sleep
from typing import Union

#The path to the configuration file. It will be loaded once on startup and contains all of the parameters that can be changed in the bot.
CONFIG_PATH = "./config/clock_config.json"
#The path to the token file. It contains the Discord API token for the bot, which can be retrieved from the Discord Developer Portal.
TOKEN_PATH = "./config/clock_token.txt"

#Type definition for the server info found in the configuration.
class ServerInfo:
	def __init__(self, id: int, channel: int) -> None:
		self.id = id
		self.channel = channel

#Type definition for the configuration. Automatically created from the configuration's json.
class Config:
	def __init__(self, json_str: str) -> None:
		obj = json.loads(json_str)
		self.update_interval: float = obj["update_interval"]
		self.time_scale: float = obj["time_scale"]
		self.time_start: datetime = datetime.strptime(obj["time_start"], "%Y-%m-%d")
		self.time_epoch: datetime = datetime.strptime(obj["time_epoch"], "%Y-%m-%d")
		self.display_format: str = obj["display_format"]
		self.servers: list[ServerInfo] = []
		for info in obj["servers"]:
			self.servers.append(ServerInfo(info["id"], info["channel"]))

#Load the configuration from CONFIG_PATH.
def get_bot_config(path: str = CONFIG_PATH) -> Config:
	try:
		file = open(path, "r")
		result = Config(file.read())
		file.close()
		return result
	except:
		print(f"Bot config was not found in {path}, could not be opened, or could not be parsed.")
		exit(1)

#Load the token from TOKEN_PATH.
def get_bot_token() -> str:
	try:
		file = open(TOKEN_PATH, "r")
		result = file.read()
		file.close()
		return result
	except:
		print(f"Bot token was not found in {TOKEN_PATH} or could not be opened.")
		exit(1)

bot_config = get_bot_config()
bot_client = discord.Client()
channels: "list[discord.VoiceChannel]" = []

#Returns the current time string based on the bot configuration.
def get_time_str() -> str:
	relative_utctime = (datetime.utcnow() - bot_config.time_epoch).total_seconds()
	scaled_time = bot_config.time_start + timedelta(seconds=relative_utctime * bot_config.time_scale)
	return scaled_time.strftime(bot_config.display_format)

#Called periodically after the bot finishes connecting to discord.
@bot_client.event
async def on_update():
	name = get_time_str()
	for channel in channels:
		try:
			print(f"Time is pending: {name}")
			await channel.edit(name=name)
			print(f"Time is now: {name}")
		except Exception as ex:
			print(f"Failed to update channel {channel.id}: {ex}")

#Called when the bot finishes connecting to discord.
@bot_client.event
async def on_ready():
	print("Bot is now online.")
	
	for server_info in bot_config.servers:
		server: Union[discord.Guild, None] = bot_client.get_guild(server_info.id)
		if server == None:
			print(f"Server {server_info.id} does not exist.")
			exit(1)
		else:
			channel: Union[discord.TextChannel, discord.VoiceChannel, None] = server.get_channel(server_info.channel)
			if channel == None:
				print(f"Channel {server_info.channel} does not exist.")
				exit(1)
			elif not isinstance(channel, discord.VoiceChannel):
				print(f"Channel {server_info.channel} is not a voice channel.")
				exit(1)
			else:
				channels.append(channel)

	class TickThread(threading.Thread):
		def run(self):
			while True:
				bot_client.dispatch("update")
				sleep(bot_config.update_interval)
	TickThread(daemon=True).start()

bot_client.run(get_bot_token())