# Data Storage
import json
import sqlite3 as db
import pandas as pd
from constants import CSV_NAME

# TODO: Find a way to handle a dict in a database, as of rn I have no clue 

# df = pd.DataFrame(columns=["ID", "XP", "Time", "Lvl"])
# df = df.append({"ID": "330075847799341076", "XP": {"ID": "330075847799341076", "810002138830471178": -1, "gaming": 1, "arts": 1, "fps": 1, "sl": 1, "dnd": 1}, "Time": 100, "Lvl": 0}, ignore_index=True)
# df = df.append({"ID": "190625917507207171", "XP": {"ID": "190625917507207171", "810002138830471178": 800, "gaming": 800, "arts": 800, "fps": 800, "sl": 800, "dnd": 1000}, "Time": 101, "Lvl": 11}, ignore_index=True)
# df = df.append({"ID": "297540904133197826", "XP": {"ID": "297540904133197826", "810002138830471178": 20, "gaming": 20, "arts": 20, "fps": 20, "sl": 20, "dnd": 3}, "Time": 102, "Lvl": 1}, ignore_index=True)
# df = df.append({"ID": "684395467722850345", "XP": {"ID": "684395467722850345", "810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)
# df = df.append({"ID": "553441706318626856", "XP": {"ID": "553441706318626856", "810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)

# sqldf = df.to_sql('data',con=sqlite3.connect('data.db'), if_exists='replace'

conn = db.connect('/data.db')

query = conn.cursor()

query.executescript("./Queries/create_tables.sql")

df = pd.DataFrame(coloumns = ["user_ID","total_XP","level","time","is_restricted"])

df = df.read_csv("./TestDataCSV/User_Info.csv")

df.to_sql(name ='User_Info', con = conn)

# ---------------------------------------------------------------

df = pd.DataFrame(columns = ["server_991178883682541700_rec_id","user_ID","server_xp"])

df.to_sql(name ='Server_991178883682541700', con = conn)

# ---------------------------------------------------------------

df = pd.DataFrame(columns = ["server_810002138830471178_rec_id","user_ID","server_xp"])

# DATA

df.to_sql(name ='Server_810002138830471178', con = conn)

# ---------------------------------------------------------------

conn.close()

df = pd.DataFrame()

df = pd.read_sql_table('User_Info', conn)

ids = df["ID"].tolist()
xps = df["XP"].tolist()

print("Sample database created",'\n')