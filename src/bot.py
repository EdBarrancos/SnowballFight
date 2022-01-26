import asyncio
import discord
from discord.ext import commands
import logging
import sys

#Local Imports
from database.database import ProfilesDB
from database.database import ItemsDB


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
        self.db_handler = DatabaseHandler(self)

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
    
    async def add_cogs(self):
        pass

    async def add_cog(self, cog : commands.Cog):
        self.owner.super().add_cog(cog)

class DatabaseHandler(Handler):
    def __init__(self, owner) -> None:
        super().__init__(owner)
        logging.debug("Initializing Databases")

        try:
            self.profile_db = ProfilesDB(self, "database/databases/testing/test_profiles.json")
            self.item_db = ItemsDB(self, "database/databases/testing/test_items.json")
        except Exception as exeption:
            logging.error("Problem Initializing Databases")
            sys.exit()

        try:
            self.init_items()
        except Exception as exption:
            logging.error("Unable to Initialize Items onto Database")
            sys.exit()

        logging.debug("Databases Initialized")

    def init_items(self):
        """
        Initializates items to the Database
        """
        logging.debug("\tInitializing Items in Databases")
        try:
            self.item_db.add_entry("Common Snowball", "Snowball")
        except Exception as exception:
            raise exception
