#Data Storage
import pandas as pd
from constants import CSV_NAME
import random as rd
import time



def load_data():
    return pd.read_csv(CSV_NAME)



def save_data(new_df,m = 'w'):
    new_df.to_csv(CSV_NAME, mode=m, index=False)


#Globals
df = load_data()



def id_exists(auth):
    global df
    
    xd = df['ID'] == auth

    if len(df.loc[xd]) != 0:
        return True

    print("Does not exist")
    return False



def add_user(id):
    global df
    data = {"ID":int(id), "XP":int(0), "Time":int(0)}
    #make temporary DataFrame

    print("\n" + str(data) + "\n")

    df = df.append(data, ignore_index=True)
    df = df.head()

    print(str(df.head()) + "\n")
    #update csv file
    print("Adding user: "+ str(id) + "... ")
    save_data(df)
    print("Done!\n")



def del_user(id):
    global df

    df = df.set_index("ID")
    df.head()

    df = df.drop(id)

    print("Dropping id: " + str(id) + "... ")
    save_data(df)
    print("Done!\n")


#move if statement to logic.py and keep XP update here
def add_xp(id):
    global df

    user_xp, user_time = grab_user_info(id)

    xp = user_xp + rd.randint(25, 50)
    df["XP"] = df["XP"].replace(to_replace= user_xp, value=xp)

    df["Time"] = df["Time"].replace(to_replace = user_time, value=int(time.time()))
    
    #Update CSV
    print("xp added")
    save_data(df)



#move if statement to logic.py and keep grab user info
def grab_user_info(id):
    global df

    ids = df["ID"].tolist()

    return df["XP"].tolist()[ids.index(id)], df["Time"].tolist()[ids.index(id)]