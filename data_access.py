# Data Storage
import pandas as pd  # Database Library
from constants import CSV_NAME, LVL_LIST  # Imports constants from 'constants.py'
import random as rd  # Random Library
import time  # Time Library


# Loads from CSV
def load_data():
    return pd.read_csv(CSV_NAME)


# Saves to CSV
def save_data(new_df, m='w'):
    new_df.to_csv(CSV_NAME, mode=m, index=False)



def load_lvls():
    return pd.read_csv(LVL_LIST, sep="\n", header=None)


# Globals
df = load_data()
lvls = load_lvls()


#Sets the time in the DataFrame
def __set_time(user_time):
    global df
    df["Time"] = df["Time"].replace(to_replace=user_time, value=int(time.time()))


# Checks if the id {auth} exists
def id_exists(auth):
    global df

    id_index = df['ID'] == auth  # gets id index from DataFrame and stores it in the variable 'id_index'

    if len(df.loc[id_index]) != 0:  # If length of the id != 0 (df.loc() is to locate)
        return True

    print("Does not exist")
    return False


# Adds user to the DataFrame and to the csv
def add_user(id):
    global df
    data = {"ID": int(id), "XP": int(0), "Time": int(0)}  # Temporary 1 item DataFrame stored in 'data'

    print("\n" + str(data) + "\n")

    df = df.append(data, ignore_index=True)  # append temp DataFrame to gloabal DataFrame
    df = df.head()

    print(str(df.head()) + "\n")
    # update csv file
    print("Adding user: " + str(id) + "... ")
    save_data(df)
    print("Done!\n")


# Deletes a user from the DataFrame and CSV
def del_user(id):
    global df

    df = df.set_index("ID")  # Sets the Index as the ID variable
    df.head()

    df = df.drop(id)  # Drops the row containing the id in 'id'

    print("Dropping id: " + str(id) + "... ")
    save_data(df)  # Drops id in CSV
    print("Done!\n")


# move if statement to logic.py and keep XP update here
def add_xp(id):
    global df

    user_xp, user_time, user_lvl = grab_user_info(id)

    xp = user_xp + rd.randint(25, 50)
    df["XP"] = df["XP"].replace(to_replace=user_xp, value=xp)

    __set_time(user_time)

    # Update CSV
    print("xp added")
    save_data(df)


#TODO: level upgrading
def add_lvl(id, amount):
    global df

    user_xp, user_time, user_lvl =  grab_user_info(id)

    lvl = user_lvl + amount
    df["Lvl"] = df["Lvl"].replace(to_replace=user_lvl, value=lvl)

    xp = lvls.loc[lvl]

    df["XP"] = df["XP"].replace(to_replace=user_xp, value=int(xp))

    __set_time(user_time)

    print("Level added and saved")
    save_data(df)


#TODO: removing levels (adjust xp accordingly?)
def remove_lvl(id, amount):
    global df

    user_xp, user_time, user_lvl =  grab_user_info(id)

    lvl = user_lvl - amount
    df["Lvl"] = df["Lvl"].replace(to_replace=user_lvl, value=lvl)

    xp = lvls.loc[lvl]

    df["XP"] = df["XP"].replace(to_replace=user_xp, value=int(xp))

    __set_time(user_time)

    print("Level removed and saved")
    save_data(df)


#TODO: clear all levels (including xp)
def clear_lvl():
    global df

    user_xp, user_time, user_lvl =  grab_user_info(id)

    lvl = 0
    df["Lvl"] = df["Lvl"].replace(to_replace=user_lvl, value=lvl)

    xp = 0

    df["XP"] = df["XP"].replace(to_replace=user_xp, value=xp)

    __set_time(user_time)

    print("Level added and saved")
    save_data(df)


# Gets the user's info (xp, time, & level)
def grab_user_info(id):
    global df

    ids = df["ID"].tolist()

    return df["XP"].tolist()[ids.index(id)], df["Time"].tolist()[ids.index(id)], df["Lvl"].tolist()[ids.index(id)]
