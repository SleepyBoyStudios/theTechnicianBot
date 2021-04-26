#Data Storage
import pandas as pd
from pandas.core.algorithms import mode
from pandas.core.indexes.base import Index
from constants import CSV_NAME
import random as rd



def add_user(id):
    data = {"ID": id, "XP": 0, "Time": 0}
    #make temporary DataFrame
    df = pd.DataFrame(columns = ['ID', 'XP', 'Time'])
    df = df.append(data, ignore_index=True)

    print(df)
    #update csv file
    save_data(df)



def del_user(id):
    df = pd.read_csv(CSV_NAME)

    df = df.set_index("ID")
    df.head()

    df = df.drop(id)
    print(df)

    print("Dropping id: " + str(id) + "...")
    save_data(df)
    print("Done!\n")



def add_xp(id):
    df = load_data()
    ids = df["ID"].tolist()
    if id in ids:
        #Add xp
        xp = df["XP"].get(ids.index(id)) + rd.randint(25, 50)
        df["XP"] = df["XP"].replace(to_replace= df["XP"].get(ids.index(id)), value=xp)
        
        #Update CSV
        save_data(df)
    
    else:
        add_user(id)



def grab_user_info(id):
    df = pd.read_csv(CSV_NAME)

    ids = df["ID"].tolist()

    if id in ids:
        return df["XP"].tolist()[ids.index(id)], df["Time"].tolist()[ids.index(id)]
    
    else:
        add_user(id)
        return False, False



def load_data():
    return pd.read_csv(CSV_NAME)


def save_data(new_df):
    new_df.to_csv(CSV_NAME, mode='w', index=False)