import random
import asyncio

# Third Party Imports
import sqlite3
import logging

from discord import guild


class DatabaseProfile():
    def __init__(self, handler) -> None:
        self.handler = handler

        self.sqlCreateItemTable = """CREATE TABLE IF NOT EXISTS items (
                                            type char(10) NOT NULL,
                                            name char(20) NOT NULL,
                                            nbr integer NOT NULL
                                        );"""
        
        self.sqlCreateLogTable = """CREATE TABLE IF NOT EXISTS logs (
                                            action char(10) NOT NULL,
                                            timestamp integer NOT NULL,
                                            cooldown integer NOT NULL
                                        );"""
        
        self.sqlCreateStatusTable = """CREATE TABLE IF NOT EXISTS status (
                                            name char(10) NOT NULL,
                                        );"""

        self.sqlCreateProfileTable = """CREATE TABLE IF NOT EXISTS profiles (
                                            player_id integer PRIMARY KEY,
                                            guild_id integer NOT NULL,
                                            points integer NOT NULL,
                                            items items,
                                            status status,
                                            logs logs
                                        );"""