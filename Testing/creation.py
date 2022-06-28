# Data Storage
import json
import sqlite3 as db
import pandas as pd
import os

# TODO: Find a way to handle a dict in a database, as of rn I have no clue 

# df = pd.DataFrame(columns=["ID", "XP", "Time", "Lvl"])
# df = df.append({"ID": "330075847799341076", "XP": {"ID": "330075847799341076", "810002138830471178": -1, "gaming": 1, "arts": 1, "fps": 1, "sl": 1, "dnd": 1}, "Time": 100, "Lvl": 0}, ignore_index=True)
# df = df.append({"ID": "190625917507207171", "XP": {"ID": "190625917507207171", "810002138830471178": 800, "gaming": 800, "arts": 800, "fps": 800, "sl": 800, "dnd": 1000}, "Time": 101, "Lvl": 11}, ignore_index=True)
# df = df.append({"ID": "297540904133197826", "XP": {"ID": "297540904133197826", "810002138830471178": 20, "gaming": 20, "arts": 20, "fps": 20, "sl": 20, "dnd": 3}, "Time": 102, "Lvl": 1}, ignore_index=True)
# df = df.append({"ID": "684395467722850345", "XP": {"ID": "684395467722850345", "810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)
# df = df.append({"ID": "553441706318626856", "XP": {"ID": "553441706318626856", "810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)

# sqldf = df.to_sql('data',con=sqlite3.connect('data.db'), if_exists='replace'
os.chdir("/home/abhi/Documents/Code-local/Python/theTechnicianBot/")

conn = db.connect('./../data.db')

query = conn.cursor()

sql_script = """ 

VACUUM;

CREATE TABLE User_Info (
    user_ID CHAR(16) PRIMARY KEY,
    total_XP INTEGER,
    level INTEGER,
    time INTEGER,
    is_restricted BOOLEAN
);

CREATE TABLE Server_991178883682541700 (
    server_991178883682541700_rec_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ID CHAR(16),
    server_xp INTEGER,
    FOREIGN KEY (user_ID) REFERENCES User_Info(user_ID)
);

CREATE TABLE Server_810002138830471178 (
    server_810002138830471178_rec_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ID CHAR(16),
    server_xp INTEGER,
    FOREIGN KEY (user_ID) REFERENCES User_Info(user_ID)
);

"""
# if (query.fetchall()) is None:
# query.executescript(sql_script)

df = pd.read_csv(r"./TestDataCSV/User_info.csv")

df.to_sql(name ='User_Info', con = conn)

# ---------------------------------------------------------------

df = pd.read_csv(r"./TestDataCSV/server_1.csv")

df.to_sql(name ='Server_991178883682541700', con = conn)

# ---------------------------------------------------------------

df = pd.read_csv(r"./TestDataCSV/server_2.csv")

df.to_sql(name ='Server_810002138830471178', con = conn)

# ---------------------------------------------------------------

conn.commit()

conn.close()

df = pd.DataFrame()

df = pd.read_sql_table('User_Info', conn)

ids = df["ID"].tolist()
xps = df["XP"].tolist()

print("Sample database created",'\n')