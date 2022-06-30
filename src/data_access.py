# Data Storage
import pandas as pd  # Database Library
from constants import DB_PATH, CSV_NAME, LVL_LIST_PATH  # Imports constants from 'constants.py'
import random as rd  # Random Library
import time  # Time Library
import json  # conversion of string to dict
import sqlalchemy as sa

# Loads table from database
def load_table(tbl: str = None) -> (Exception / pd.DataFrame):
    return Exception('No table to load DataFrame from') if tbl is None else pd.read_sql_table(tbl, sa.create_engine(f"sqlite://{DB_PATH}"))

# Saves to CSV
def save_data(new_df: pd.DataFrame, m: str = 'w'):
    new_df.to_csv(CSV_NAME, mode=m, index=False)

# Saves table from database
def save_table(new_df: pd.DataFrame, tbl: str = None):
    if tbl is None:
        return Exception('No table to save DataFrame in') 
    new_df.to_sql(tbl, sa.create_engine(f"sqlite://{DB_PATH}"))

# Loads levels from CSV
def load_lvls() -> pd.DataFrame:
    return pd.read_csv(LVL_LIST_PATH, sep=",", header=None)


def grab_restricted_list() -> list:
    with open('restricted.json') as file:
        return json.load(file)


def store_restricted_list(list: list):
    with open('restricted.json','w') as file:
        json.dump(list, indent=4, fp=file)


# Globals
df_user_info = load_table(tbl='user_info')
df_child_table = pd.DataFrame()
lvls = load_lvls()


# returns dataframe
def load_dataframe():
    return df


# Sets the time in the DataFrame
def __set_time(user_time) -> int:
    global df
    df["Time"] = df["Time"].replace(to_replace=user_time, value=int(time.time()))

def calc_xp(id):
    global df

    user_xp, user_time, user_lvl = grab_user_info(id)

    return sum(user_xp.values())


# Checks if the id {user_id} exists
async def id_exists(user_id) -> (int / bool):
    global df_user_info

    user = df_user_info.loc(await df_user_info.index(user_id))  # gets id index from DataFrame and stores it in the variable 'id_index'

    # If length of the id != 0 (df.loc() is to locate)
    return user if len(user) != 0 else False


# Adds user to the DataFrame and to the database
async def add_user(user_id: int):
    global df_user_info
    data = {"user_ID": user_id, "total_XP": 0, "level": 0, "time": 0} # Temporary 1 item DataFrame stored in 'data'

    print(f'\n{data}\n')

    df_user_info = await df_user_info.append(data, ignore_index=True)  # append temp DataFrame to global DataFrame
    df_user_info = await df_user_info.head()

    print(f'{df_user_info.head()}\n')

    # update database
    print(f"Adding user: {user_id}... ")

    e = await save_table(new_df=df_user_info, tbl='User_Info')
    if e is not None: print(e)

    print("Done!\n")


# Deletes a user from the DataFrame and CSV
def del_user(id):
    global df

    df = df.set_index("ID")  # Sets the Index as the ID variable
    df.head()

    df = df.drop(id)  # Drops the row containing the id in 'id'

    print(f"Dropping id: {str(id)}... ")
    save_data(df)  # Drops id in CSV
    print("Done!\n")


# move if statement to logic.py and keep XP update here
def add_xp(id, server, amount=0):
    global df

    user_xp, user_time, user_lvl = grab_user_info(id)

    xp = user_xp.copy()
    xp[str(server)] = (user_xp.get(str(server)) + amount if amount != 0 else rd.randint(25, 50))

    df["XP"] = df["XP"].replace(to_replace=str(user_xp), value=str(xp))

    __set_time(user_time)

    # Update CSV
    print("xp added")
    save_data(df)


# level upgrading
def add_lvl(id, amount=1):
    global df, lvls

    user_xp, user_time, user_lvl = grab_user_info(id)

    lvl = user_lvl + amount
    df["Lvl"] = df["Lvl"].replace(to_replace=user_lvl, value=lvl)

    lvl_xp = lvls.loc[int(lvl) + 1, 0]

    lvl_xp = int(lvl_xp.split(",")[1])

    server_amount = len(user_xp.keys())

    lvl_xp -= sum(user_xp.values())

    for _ in range(server_amount):
        x = lvl_xp // server_amount
        add_xp(str(id), list(user_xp.keys())[_], x)

    if lvl_xp % server_amount != 0:
        mod_amount = lvl_xp % server_amount
        for _ in range(mod_amount):
            add_xp(str(id), list(user_xp.keys())[_], 1)

    __set_time(user_time)

    print("Level added and saved")
    save_data(df)


# TODO: removing levels (adjusts xp accordingly) ASK ABOUT HOW TO REMOVE LEVELS
def remove_lvl(id, amount):
    global df

    user_xp, user_time, user_lvl = grab_user_info(id)

    lvl = user_lvl - amount
    df["Lvl"] = df["Lvl"].replace(to_replace=user_lvl, value=lvl)

    xp = lvls.loc[lvl]

    df["XP"] = df["XP"].replace(to_replace=user_xp, value=int(xp))

    __set_time(user_time)

    print("Level removed and saved")
    save_data(df)


# clear all levels (including xp)
def clear_lvl(id):
    global df

    user_xp, user_time, user_lvl = grab_user_info(id)

    lvl = 0
    df["Lvl"] = df["Lvl"].replace(to_replace=user_lvl, value=lvl)

    xp = user_xp.fromkeys(user_xp.iterkeys(), 0)
    df["XP"] = df["XP"].replace(to_replace=user_xp, value=xp)

    __set_time(user_time)

    print("Level added and saved")
    save_data(df)


# Gets the user's info (xp, time, & level)
def grab_user_info(user):
    global df_user_info

    ids = [str(x) for x in df["user_ID"].tolist()]

    xp_str = df["XP"][ids.index(str(user))]
    print(xp_str.replace("\'", '\"'))
    xp_dict = json.loads(xp_str.replace("\'", '\"'))
    return xp_dict, df["Time"].tolist()[ids.index(str(user))], df["Lvl"].tolist()[ids.index(str(user))]



