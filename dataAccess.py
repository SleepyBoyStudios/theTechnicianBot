#Data Storage
import pandas as pd
import constants as const

#constants

def add_user(id):
    data = {"ID": id, "XP": 0, "Time": 0}
    #make temporary DataFrame
    df = pd.DataFrame(columns = ['ID', 'XP', 'Time'])
    df = df.append(data, ignore_index=True)

    print(df)
    #update csv file
    df.to_csv(const.CSV_NAME, mode='a', index=False)

def del_user():
    return

def edit_user():
    return

def add_xp(id):
    ids = pd.read_csv(const.CSV_NAME)["ID"].tolist()
    if id in ids:
        #Add xp
        return
    
    else:
        add_user(id)

def grab_user_info(id):
    df = pd.read_csv(const.CSV_NAME)

    ids = df["ID"].tolist()

    if id in ids:
        return df["XP"].tolist()[ids.index(id)], df["Time"].tolist()[ids.index(id)]
    
    else:
        add_user(id)
        return False, False


#def loadData()
#def saveData()