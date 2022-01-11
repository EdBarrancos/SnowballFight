import asyncio
import discord
from discord.ext import commands
import logging

# from decouple import config

import os

#Local Imports
from bot import MyBot
import keep_alive


# logging.basicConfig(format='%(levelname)s:%(message)s', 
#                    filename="../bot_logs/snowman.log", 
#                    level=logging.DEBUG, filemode="w")


myBot = MyBot(("!", "$"))

keep_alive.keep_alive()

myBot.run(os.getenv('token'))

# myBot.run(config("token"))