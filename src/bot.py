import asyncio

import discord
from discord.ext import commands
import logging

#Local Imports
from database.database import DatabaseProfile 


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        logging.info("Intializing Bot...")
        super().__init__(*args, **kwargs)
        logging.info("Bot Initialized Successfully")


    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')

        print('-------')

        print("Initializing Handlers")

        self.cogHandler = CogHandler(self)

        print("Handlers Initialized")

        print('-------')


    async def on_guild_join(self, guild):
        logging.info(f'Guild {guild.name} joined')


    async def on_guild_remove(self, guild):
        logging.info(f'Guild {guild.name} left')

    
    async def on_message(self, message):
        if message.author != self.user:
            logging.info(f'Message received {message.content}')
            await message.channel.send(message.content)
            return await super().on_message(message)


class Handler():
    def __init__(self, owner) -> None:
        self.owner = owner


class CogHandler(Handler):
    def __init__(self, owner) -> None:
        super().__init__(owner)
    
    async def addCogs(self):
        pass

    async def addCog(self, cog : commands.Cog):
        self.owner.super().add_cog(cog)

class DatabaseHandler(Handler):
    def __init__(self, owner) -> None:
        super().__init__(owner)
        self.proDatabase = DatabaseProfile(self)
