# Data Storage
import pandas as pd  # Database Library
from constants import CSV_NAME, LVL_LIST  # Imports constants from 'constants.py'
import random as rd  # Random Library
import time  # Time Library
import json  # conversion of string to dict
import re # frickin regex bs


# Loads from CSV
def load_data():
    return pd.read_csv(CSV_NAME)


# Saves to CSV
def save_data(new_df, m='w'):
    new_df.to_csv(CSV_NAME, mode=m, index=False)


# Loads levels from CSV
def load_lvls():
    return pd.read_csv(LVL_LIST, sep=",", header=None)


def grab_restricted_list():
    with open('restricted.json') as file:
        return json.load(file)


def store_restricted_list(list):
    with open('restricted.json','w') as file:
        json.dump(list, indent=4, fp=file)


# Globals
df = load_data()
lvls = load_lvls()


# returns dataframe
def load_dataframe():
    return df


# Sets the time in the DataFrame
def __set_time(user_time):
    global df
    df["Time"] = df["Time"].replace(to_replace=user_time, value=int(time.time()))


# TODO: Calculates total xp
def calc_xp(id):
    global df

    user_xp, user_time, user_lvl = grab_user_info(id)

    return sum(user_xp.values())


# Checks if the id {id} exists
def id_exists(id):
    global df

    id_index = df['ID'] == id  # gets id index from DataFrame and stores it in the variable 'id_index'

    if len(df.loc[id_index]) != 0:  # If length of the id != 0 (df.loc() is to locate)
        return True

    print("Does not exist")
    return False


# Adds user to the DataFrame and to the csv
def add_user(id):
    global df
    data = {"ID": str(id), "XP": 0, "Time": 0} # Temporary 1 item DataFrame stored in 'data'

    print("\n" + str(data) + "\n")

    df = df.append(data, ignore_index=True)  # append temp DataFrame to global DataFrame
    df = df.head()

    print(str(df.head()) + "\n")
    # update csv file
    print(f"Adding user: {str(id)}... ")
    save_data(df)
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
    global df

    ids = [str(x) for x in df["ID"].tolist()]

    xp_str = df["XP"][ids.index(str(user))]
    print(xp_str.replace("\'", '\"'))
    xp_dict = json.loads(xp_str.replace("\'", '\"'))
    return xp_dict, df["Time"].tolist()[ids.index(str(user))], df["Lvl"].tolist()[ids.index(str(user))]



