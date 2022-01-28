import asyncio
import json
import os

# Third Party Imports
import logging


class Database:
    """
    Main Database class

    ...

    Attributes
    ----------
    hanlder : obj
        Obj which has initialized the database
    file : str
        Location of the database file
    """
    ################
    #BASE FUNCTIONS#
    ################

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
        #Verify path for file as correct
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
        logging.debug("Dumping into database")
        try:
            json.dump(self.db , open(self.location, "w+"), indent=4)
            return True
        except:
            raise Exception("Error dumping data into database")

    def destroy(self):
        logging.debug("Destroying database")
        self.clear()
        os.remove(self.location)

    def clear(self):
        logging.debug("Clearing Database")
        self.db = dict()
        self.dumpdb()

    ######
    #GETS#
    ######

    def get_instance(self, id) -> list:
        if type(id) != str:
            id = str(id)
        return self.db[id]

    def get_first_entryid_with(self, entry) -> int:
        """ Returns the first entry's id with the same corresponding values"""
        try:
            for id in self.get_ids():
                found = True
                inst = self.get_instance(id)
                for k in list(entry.keys()):

                    if inst[k] != entry[k]:
                        found = False
                        break
                if found:
                    return id
            return None
        except Exception as exception:
            raise exception


    def get_collumn(self, key) -> list:
        if len(self.get_ids()) == 0:
            raise Exception("Empty Database")
        if key not in self.db[self.get_ids()[0]].keys():
            raise Exception("Key does not exist in database")
        try:
            collumn = list()
            for id in self.get_ids():
                collumn.append(self.db[id][key])
        except Exception as exception:
            raise exception
        return collumn

    def get_keys(self) -> list:
        if len(self.get_ids()) == 0:
            raise Exception("Empty Database")
        try:
            return self.db[self.get_ids()[0]].keys()
        except Exception as exception:
            raise exception

    def get_ids(self) -> list:
        return list(self.db.keys())

    def get_next_id(self):
        try:
            ids = self.get_ids()
        except:
            return 0
        if len(ids) == 0:
            return 0
        return int(ids[len(ids) - 1]) + 1

    def get_all_entries(self):
        return self.db

    
    async def add_entry(self, dct : dict):
        logging.debug("Adding Entry")
        try:
            for key in dct.keys():
                if type(key) != str:
                    key = str(key)
                self.db[key] = dct[key]
                self.dumpdb()
                return True
        except Exception as exception:
            logging.error("Error adding entry to database")
            raise exception
            
    
    async def update_entry(self, id, new_entry):
        try:
            self.db[id] = new_entry
            self.dumpdb()
            return True
        except Exception as exception:
            logging.error("Error updating entry to database")
            raise exception

    def entry_exists(self, entry: dict) -> bool:
        try:
            ids = self.get_ids()
            for id in ids:
                if self.get_instance(id) == entry:
                    return True
        except:
            return False
        return False
    
    async def similar_entry(self, entry: dict) -> bool:
        """ You can only enter part of the parameters.
            If there is a entry with the same values in those parameters,
                returns True
            Else
                returns False """
        try:
            for id in self.get_ids():
                found = True
                inst = self.get_instance(id)
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
    def __init__(self, handler, file) -> None:
        super().__init__(handler, file)
    
    async def add_entry(self, type : str, name : str):
        if not await self.entry_exists({"type": type,"name": name}):
            try:
                await super().add_entry({str(self.get_next_id()): {"type": type, "name": name}})
            except Exception as exception:
                raise exception
            return True
        return False



class ProfilesDB(Database):
    def __init__(self, handler, file) -> None:
        super().__init__(handler, file)
        #id
            #player_id
            #guild_id
            #items [(id,nbr), ...]
            #points
            #status effect(DONT KNOW YET)
            #logs [(activity name, timestamp, total cooldown)]

    async def add_entry(self, player_id = 0, guild_id = 0, items = None, points = 0, status = None, logs = None):
        dct = {str(self.get_next_id()): {"player_id": player_id, "guild_id": guild_id,
            "items": (list() if items == None else items), "points": points, "status": None,
            "logs": list() if logs == None else logs}}
        return await super().add_entry(dct)
    
    async def create_profile(self, player_id : int, guild_id : int):
        try:
            if await self.similar_entry({"player_id": player_id, "guild_id": guild_id}):
                return False
            return await self.add_entry(player_id=player_id, guild_id=guild_id)
        except Exception as e:
            raise e
    
    async def update_item(self, profile_id: int, item_id: int, item_count = 0):
        if profile_id is None:
            raise Exception("Invalid Player Id")
        if item_id < 0:
            raise Exception("Invalid Item Id")
        try:
            profile = self.get_instance(str(profile_id))
            if await self.item_exists_in_profile(profile, item_id):
                for item in profile["items"]:
                    if item[0] == item_id:
                        item[1] += item_count
            else:
                profile["items"].append([item_id, item_count])

            await self.update_entry(str(profile_id), profile)
            
        except Exception as exception:
            raise exception
    
    async def item_exists_in_profile(self, profile, item_id):
        for item in profile["items"]:
            if item[0] == item_id:
                return True
        return False
    
    async def get_profiles(self, player_id = None, guild_id = None) -> list:
        try:
            lst = list()
            entries = self.get_all_entries()
            for entry in entries:
                if player_id is not None:
                    if entries[entry]["player_id"] == player_id:
                        lst.append(entries[entry])
                elif guild_id is not None:
                    if entries[entry]["guild_id"] == guild_id:
                        lst.append(entries[entry])
                else:
                    lst.append(entries[entry])
        except Exception as exception:
            raise exception
        return lst
    
    async def does_profile_exist(self):
        pass
        