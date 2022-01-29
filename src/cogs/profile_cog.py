import discord
from discord.ext import commands
import logging
import sys

from database.database import ProfilesDB
from database.database import ItemsDB

class ProfileCog(commands.Cog):
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

    name = "profile"
    aliases = tuple()
    helpMessage = ""
    briefMessage = ""
    @commands.command(name=name, aliases=aliases, help=helpMessage, brief=briefMessage)
    async def profile_command(self, ctx):
        if not await self.profile_db.does_profile_exist(ctx.author.id, ctx.guild.id):
            try:
                await self.profile_db.create_profile(ctx.author.id, ctx.guild.id)
            except Exception as _:
                await ctx.send("Error while creating profile")
                return
        try:
            profile = await self.profile_db.get_profiles(player_id=ctx.author.id, guild_id=ctx.guild.id)
            embed = discord.Embed(title=ctx.guild.get_member(profile[0]["player_id"]).name)
            
            embed.add_field(name="Points", value=profile[0]["points"])
            await ctx.send(embed=embed)
        except Exception as _:
            await ctx.send("Error while creating embed")
            
