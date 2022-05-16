""" database.py

A Module with classes and functions to manage and maintain the Databases in this project

Contains a Database class that has low level management functions
It also has more specific classes which inherit the main Database class
"""

# Third Party Imports
import logging
import json
import os

class Database:
    """
    Main Database class

    ...

    Attributes
    ----------
    handler : obj
        Obj which has initialized the database
    file : str
        Location of the database file
    """

    def __init__(self, handler, file) -> None:
        """
        Constructs all the necessary attributes for the Database object.

        Parameters
        ----------
            hanlder : obj
                Obj which has initialized the database
            file : str
                Location of the database file
        """

        logging.debug("Initializing Database")
        self.handler = handler
        self.location = os.path.expanduser(file)
        #TODO: Verify path for file as correct
        self.load(self.location)

    def load(self , location : str):
        """
        Loads the File from the asserted location or creates the file

        Parameters
        ----------
            location : str
                Location of the database file
        """

        logging.debug("\tLoading Database File")
        if os.path.exists(location):
            self._load()
        else:
            self.db = dict()
            self.dumpdb()
        logging.debug("\tDatase Loaded")
        return True

    def _load(self):
        """
        Loads the content on the database file into a local variable
        """

        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        """
        Dumps the content on the local database into its file
        """

        logging.debug("Dumping into database")
        try:
            json.dump(self.db , open(self.location, "w+"), indent=4)
            return True
        except:
            raise Exception("Error dumping data into database")

    def destroy(self):
        """
        Erases the information on the local database and deletes the file
        """

        logging.debug("Destroying database")
        self.clear()
        os.remove(self.location)

    def clear(self):
        """
        Erases the information on the local database
        """

        logging.debug("Clearing Database")
        self.db = dict()
        self.dumpdb()

    def get_entry(self, key : int) -> dict:
        """
        Returns the entry associated with the given id

        Parameters
        ----------
            key : int
                Entry's Id

        Return
        ------
            type : dict
            Returns Entry of the corresponding key
        """

        if isinstance(key,str):
            key = str(key)
        return self.db[key]

    def get_entry_key_w(self, entry_parameters : dict) -> int:
        """
        Returns the first entry's id with the same corresponding values

        Parameters
        ----------
            entry_parameters : dict
                The Parameters to search for in the database

        Return
        ------
            type : int
            Returns the First Key of the Entry that has the corresponding paramters
        """
    
        #TODO: Improve?
        try:
            for key in self.get_keys():
                found = True
                inst = self.get_entry(key)
                for k in list(entry_parameters.keys()):

                    if inst[k] != entry_parameters[k]:
                        found = False
                        break
                if found:
                    return id
            return None
        except Exception as exception:
            raise exception


    def get_collumn(self, entry_parameters : dict) -> list:
        """
        Returns a list with the values of the parameter in each entry

        Parameters
        ----------
            entry_parameters : dict
                The Parameters to search for in the database

        Return
        ------
            type : list
            Returns a list with the values of the parameter in each entry
        """

        if len(self.get_keys()) == 0:
            raise Exception("Empty Database")
        if entry_parameters not in self.db[self.get_keys()[0]].keys():
            raise Exception("Parameter does not exist in database")
        try:
            collumn = list()
            for key in self.get_keys():
                collumn.append(self.db[key][entry_parameters])
        except Exception as exception:
            raise exception
        return collumn

    def get_parameters(self) -> list:
        """
        Returns a list with all the parameters

        Return
        ------
            type : list
            Returns a list with all the parameters
        """

        if len(self.get_keys()) == 0:
            raise Exception("Empty Database")
        try:
            return self.db[self.get_keys()[0]].keys()
        except Exception as exception:
            raise exception

    def get_keys(self) -> list:
        """
        Returns a list with all the keys in the database

        Return
        ------
            type : list
            Returns a list with all the keys in the database
        """

        return list(self.db.keys())

    def get_next_key(self) -> int:
        """
        Returns the next available key

        Return
        ------
            type : int
            Returns the next available key
        """

        try:
            keys = self.get_keys()
        except:
            return 0
        if len(keys) == 0:
            return 0
        return int(keys[len(keys) - 1]) + 1

    def get_all_entries(self) -> dict:
        """
        Returns the whole database

        Return
        ------
            type : dict
            Returns the whole database
        """

        return self.db

    def add_entry(self, entry_to_add : dict):
        """
        Adds an entry to the database

        Parameters
        ------
            entry_to_add : dict
                Entry to be added to the database
        """

        #TODO: Options to check if entry exists or not
        #TODO: Receive only dict with parameters and calculate the next key here
        logging.debug("Adding Entry")
        try:
            for key in entry_to_add.keys():
                if not isinstance(key, str):
                    key = str(key)
                self.db[key] = entry_to_add[key]
                self.dumpdb()
                return True
        except Exception as exception:
            logging.error("Error adding entry to database")
            raise exception

    async def update_entry(self, key : int, new_entry : dict):
        """
        Updates an entry already in the database

        Parameters
        ------
            key : int
                Key of the Entry to update
            new_entry : dict
                Updated version of the Entry
        """

        try:
            #TODO: Check for Entry existance
            self.db[key] = new_entry
            self.dumpdb()
            return True
        except Exception as exception:
            logging.error("Error updating entry to database")
            raise exception

    def entry_exists(self, entry: dict) -> bool:
        """
        Check if Entry exists in database

        Parameters
        ------
            entry : dict
                Entry to check

        Return
        ------
            type : bool
            Returns True if entry exists, False otherwise
        """

        keys = self.get_keys()
        for key in keys:
            if self.get_entry(key) == entry:
                return True
        return False

    async def similar_entry(self, entry: dict) -> bool:
        """
        Checks if an entry with the same values to the same parameters exists

        Parameters
        ----------
            entry : dict
                The Parameters to search a similar entry for

        Return
        ------
            type : bool
            True if entry found, False otherwise
        """

        #TODO: Improve?
        try:
            for key in self.get_keys():
                found = True
                inst = self.get_entry(key)
                for k in list(entry.keys()):
                    if inst[k] != entry[k]:
                        found = False
                        break
                if found:
                    return True
            return False
        except Exception as exception:
            raise exception



class ItemsDB(Database):
    """
    Items Database Class

    Database to store the existing items in the system

    ...

    Attributes
    ----------
    handler : obj
        Obj which has initialized the database
    file : str
        Location of the database file

    ...

    Database Organization
    ---------------------
    key
        type : str
            Item type
        name : str
            Item's name
    """

    def add_item(self, item_type : str, item_name : str) -> bool:
        """
        Add Item to the Database
        
        Parameters
        ----------
            item_type : str
                Item's type
            item_name : str
                Item's name

        Return
        ------
            type : bool
            True if Item is added, False if it already exists in the database
        """

        if not self.entry_exists({"type": item_type,"name": item_name}):
            super().add_entry({str(self.get_next_key()): {"type": item_type, "name": item_name}})
            return True
        return False



class ProfilesDB(Database):
    """
    Profile Database Class

    Database to store the profiles in the system

    ...

    Attributes
    ----------
    handler : obj
        Obj which has initialized the database
    file : str
        Location of the database file

    ...

    Database Organization
    ---------------------
    key
        player_id : str
            Owner's Id inside Discord
        guild_id : str
            Guild's Id the Profile exists in
        items : list : [(item's id, item's count on the profile), ...]
            List of Items in the players possession
        points : int
            Profile's Points
        status effect : Unknown
            Future Feature?
        logs : list : [(action's name, init timestamp, total cooldown), ...]
            Log of profile's action in order to keep track of cooldowns
    """

    def add_profile(self, player_id = 0, guild_id = 0, items = None, points = 0, status = None, logs = None):
        """
        Add Profile to the Database

        Parameters
        ----------
            player_id[Optionl] : int[0]
                Owner's Id inside Discord
            guild_id[Optionl] : int[0]
                Guild's Id the Profile exists in
            items[Optionl] : list[None] : [(item's id, item's count on the profile), ...]
                List of Items in the players possession
            points[Optionl] : int[0]
                Profile's Points
            status effect[Optionl] : Unknown[None]
                Future Feature?
            logs[Optionl] : list[None] : [(action's name, init timestamp, total cooldown), ...]
                Log of profile's action in order to keep track of cooldowns

        Return
        ------
            type : bool
            True if Item is added, False if it already exists in the database
        """
        dct = {str(self.get_next_key()): {"player_id": player_id, "guild_id": guild_id,
            "items": list() if items is None else items, "points": points,
            "status": None if status is None else status,
            "logs": list() if logs is None else logs}}
        return super().add_entry(dct)

    async def create_profile(self, player_id : int, guild_id : int) -> bool:
        """
        Creates Empty Profile in the Database

        Parameters
        ----------
            player_id : int
                Owner's Id inside Discord
            guild_id : int
                Guild's Id the Profile exists in

        Return
        ------
            type : bool
            True if profile added to the database, False otherwise
        """

        if await self.similar_entry({"player_id": player_id, "guild_id": guild_id}):
            return False
        return self.add_profile(player_id=player_id, guild_id=guild_id)

    async def update_item(self, profile_key: int, item_key: int, item_count = 1):
        """
        Update Items in a Profile

        Parameters
        ----------
            profile_key : int
                Profile's key
            item_key : int
                Item's Key to be added to the Profile
            item_count[Optional] : int[1]
                Number of Item's to add to the Profile
        """

        #TODO: Delete Item from List if Count reaches to 0
        if profile_key is None:
            raise Exception("Invalid Player Id")
        if item_key < 0:
            raise Exception("Invalid Item Id")
        try:
            profile = self.get_entry(str(profile_key))
            if await self.item_exists_in_profile(profile, item_key):
                for item in profile["items"]:
                    if item[0] == item_key:
                        item[1] += item_count
            else:
                profile["items"].append([item_key, item_count])

            await self.update_entry(str(profile_key), profile)
        except Exception as exception:
            raise exception

    async def item_exists_in_profile(self, profile : dict, item_key : int) -> bool:
        """
        Check if Profile is the possession of an item

        Parameters
        ----------
            profile : dict
                Profile
            item_key : int
                Item's Key to be added to the Profile

        Return
        ------
            type : bool
            True if item exists in profile, False otherwise
        """

        for item in profile["items"]:
            if item[0] == item_key:
                return True
        return False

    async def get_profiles(self, player_id = None, guild_id = None) -> list:
        """
        Get Profiles with optional search paramteres

        Parameters
        ----------
            player_id[Optional] : int[None]
                Owner's Id inside Discord
            guild_id[Optional] : int[None]
                Guild's Id the Profile exists in

        Return
        ------
            type : list
            List of profiles found
        """

        lst = list()
        entries = self.get_all_entries()
        for entry in entries:
            if player_id is not None and guild_id is not None:
                if entries[entry]["player_id"] == player_id:
                    if entries[entry]["guild_id"] == guild_id:
                        lst.append(entries[entry])
            elif player_id is not None:
                if entries[entry]["player_id"] == player_id:
                    lst.append(entries[entry])
            elif guild_id is not None:
                if entries[entry]["guild_id"] == guild_id:
                    lst.append(entries[entry])
            else:
                lst.append(entries[entry])
        return lst

    async def does_profile_exist(self, player_id : int, guild_id : int) -> bool:
        """
        Check if Profile Exists

        Parameters
        ----------
            player_id : int
                Owner's Id inside Discord
            guild_id : int
                Guild's Id the Profile exists in

        Return
        ------
            type : bool
            True if profile exists, False otherwise
        """

        return len(await self.get_profiles(player_id=player_id, guild_id=guild_id)) != 0
        