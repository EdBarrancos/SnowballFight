import database as db

items = db.ItemsDB("hello","src/database/databases/testing/test.json")

items.add_entry("bola", "bola de gelo")
items.add_entry("faca", "faca de cortar")
items.add_entry("bola", "bola de fogo")
items.add_entry("bola", "bola de gelo")
items.clear()