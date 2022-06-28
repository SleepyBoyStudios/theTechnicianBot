# Data Storage
import json
import sqlite3 as db
import pandas as pd
from constants import CSV_NAME

# TODO: Find a way to handle a dict in a database, as of rn I have no clue 

df = pd.DataFrame(columns=["ID", "XP", "Time", "Lvl"])
df = df.append({"ID": "330075847799341076", "XP": {"ID": "330075847799341076", "810002138830471178": -1, "gaming": 1, "arts": 1, "fps": 1, "sl": 1, "dnd": 1}, "Time": 100, "Lvl": 0}, ignore_index=True)
df = df.append({"ID": "190625917507207171", "XP": {"ID": "190625917507207171", "810002138830471178": 800, "gaming": 800, "arts": 800, "fps": 800, "sl": 800, "dnd": 1000}, "Time": 101, "Lvl": 11}, ignore_index=True)
df = df.append({"ID": "297540904133197826", "XP": {"ID": "297540904133197826", "810002138830471178": 20, "gaming": 20, "arts": 20, "fps": 20, "sl": 20, "dnd": 3}, "Time": 102, "Lvl": 1}, ignore_index=True)
df = df.append({"ID": "684395467722850345", "XP": {"ID": "684395467722850345", "810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)
df = df.append({"ID": "553441706318626856", "XP": {"ID": "553441706318626856", "810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)

# sqldf = df.to_sql('data',con=sqlite3.connect('data.db'), if_exists='replace'

#! This doesn't work because of the way sqlite handles dictionares. We cant just store a dictionary as one WHOLE value

conn = db.connect('./data.db')
df.to_sql(name ='database', con = db.connect('./data.db'), if_exists='replace')

conn.close()

df = pd.DataFrame()

df = pd.read_sql_table('data', con=db.connect('data.db'))

ids = df["ID"].tolist()
xps = df["XP"].tolist()

# Create Restricted List
with open('restricted.json', 'w') as json_file:
    json.dump(["<!@402319880860467201>"], indent = 4,fp=json_file)


print("Sample database created",'\n')