import json
import os

# Third Party Imports
import logging


class Database:
    def __init__(self, handler, file) -> None:
        logging.debug("Initializing Database")
        self.handler = handler
        self.location = os.path.expanduser(file)
        #Verify path for file as correct
        self.load(self.location)

    def load(self , location):
        logging.debug("\tLoading Database File")
        if os.path.exists(location):
            self._load()
        else:
            self.db = dict()
            self.dumpdb()
        logging.debug("\tDatase Loaded")
        return True

    def _load(self):
        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        logging.debug("Dumping into database")
        try:
            json.dump(self.db , open(self.location, "w+"), indent=4)
            return True
        except:
            raise Exception("Error dumping data into database")
    
    def add_entry(self, dct : dict):
        logging.debug("Adding Entry")
        try:
            for key in dct.keys():
                self.db[key] = dct[key]
                self.dumpdb()
                return True
        except Exception as e:
            logging.error("Error adding entry to database")
            raise e

    def get_instance(self, id) -> list:
        return self.db[id]

    def get_collumn(self, key) -> list:
        if len(self.get_ids()) == 0:
            raise Exception("Empty Database")
        if key not in self.db[self.get_ids()[0]].keys():
            raise Exception("Key does not exist in database")
        try:
            collumn = list()
            for id in self.get_ids():
                collumn.append(self.db[id][key])
        except Exception as e:
            raise e
        return collumn

    def get_keys(self) -> list:
        if len(self.get_ids()) == 0:
            raise Exception("Empty Database")
        try:
            return self.db[self.get_ids()[0]].keys()
        except Exception as e:
            raise e
            

    def entry_exists(self, entry: dict) -> bool:
        try:
            ids = self.get_ids()
            for id in ids:
                if self.get_instance(id) == entry:
                    return True
        except:
            return False
        return False
    
    def similar_entry(self, entry: dict) -> bool:
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
                if(found):
                    return True
            return False
        except Exception as e:
            raise e
    
    def get_ids(self) -> list:
        print(list(self.db.keys()))
        return list(self.db.keys())

    def get_next_id(self):
        try:
            ids = self.get_ids()
        except Exception as _:
            return 0
        if len(ids) == 0:
            return 0
        return int(ids[len(ids) - 1]) + 1

    def destroy(self):
        logging.debug("Destroying database")
        self.clear()
        os.remove(self.location)

    def clear(self):
        logging.debug("Clearing Database")
        self.db = dict()
        self.dumpdb()



class ItemsDB(Database):
    def __init__(self, handler, file) -> None:
        super().__init__(handler, file)
    
    def add_entry(self, type : str, name : str):
        if not self.entry_exists({"type": type,"name": name}):
            try:
                super().add_entry({str(self.get_next_id()): {"type": type, "name": name}})
            except Exception as e:
                raise e
            return True
        else:
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

    def add_entry(self, player_id = 0, guild_id = 0, items = None, points = 0, status = None, logs = None):
        dct = {str(self.get_next_id()): {"player_id": player_id, "guild_id": guild_id,
            "items": (list() if items == None else items), "points": points, "status": None,
            "logs": list() if logs == None else logs}}
        return super().add_entry(dct)
    
    def create_profile(self, player_id : int, guild_id : int):
        try:
            if self.similar_entry({"player_id": player_id, "guild_id": guild_id}):
                raise Exception("Profile Already exists")
            self.add_entry(player_id=player_id, guild_id=guild_id)
        except Exception as e:
            raise e
        