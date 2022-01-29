import asyncio
import discord
from discord.ext import commands
import logging
from decouple import config

#Local Imports
from src.bot import MyBot


logging.basicConfig(format='%(levelname)s:%(message)s',
                    filename="bot_logs/snowman.log",
                    level=logging.DEBUG, filemode="w")

intents = discord.Intents.default()
intents.members = True

myBot = MyBot(("!", "$"), intents=intents)

# keep_alive.keep_alive()

# myBot.run(os.getenv('token'))

myBot.run(config("token"))