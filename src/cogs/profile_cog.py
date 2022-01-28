import discord
from discord.ext import commands
import logging
import sys

from database.database import ProfilesDB
from database.database import ItemsDB

class Profile_Cog(commands.cog):
    def __init__(self, handler):
        self.handler = handler

        logging.debug("Initializing Databases")

        try:
            self.profile_db = ProfilesDB(self, "database/databases/testing/test_profiles.json")
            self.item_db = ItemsDB(self, "database/databases/testing/test_items.json")
        except Exception as _:
            logging.error("Problem Initializing Databases")
            sys.exit()

        try:
            self.init_items()
        except Exception as _:
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