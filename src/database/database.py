import random
import asyncio
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
        return True

    def _load(self):
        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        try:
            json.dump(self.db , open(self.location, "w+"), indent=4)
            return True
        except:
            raise Exception("Error dumping data into database")
    
    def add_entry(self, dct : dict):
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

    def get_collumn(self, key):
        pass

    def get_keys(self):
        pass

    def entry_exists(self, entry: dict) -> bool:
        try:
            ids = self.get_ids()
            for id in ids:
                if self.get_instance(id) == entry:
                    return True
        except:
            return False
        return False
    
    def get_ids(self) -> list:
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
        self.clear()
        os.remove(self.location)

    def clear(self):
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
        