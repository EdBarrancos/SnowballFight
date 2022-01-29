import asyncio
import discord
from discord.ext import commands
import logging
import sys

#Local Imports
from .cogs.profile_cog import ProfileCog


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        logging.info("Intializing Bot...")
        super().__init__(*args, **kwargs)
        logging.info("Bot Initialized Successfully")


    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')

        print('-------')

        print("Initializing Handlers")

        self.cog_handler = CogHandler(self)

        print("Handlers Initialized")

        print('-------')


    async def on_guild_join(self, guild):
        logging.info(f'Guild {guild.name} joined')


    async def on_guild_remove(self, guild):
        logging.info(f'Guild {guild.name} left')


class Handler():
    def __init__(self, owner) -> None:
        self.owner = owner


class CogHandler(Handler):
    def __init__(self, owner) -> None:
        super().__init__(owner)
        self.add_cogs()
    
    def add_cogs(self):
        self.add_cog(ProfileCog(self))

    def add_cog(self, cog : commands.Cog):
        self.owner.add_cog(cog)
