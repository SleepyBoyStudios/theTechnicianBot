#Data Storage
import pandas as pd

def add_xp(id):
    ids = pd.read_csv("data.csv")["ID"].tolist()
    if id in ids:
        #Add xp
        return
    
    else:
        addUser(id)

def add_user(id):
    data = {"ID": id, "XP": 0, "Time": 0}

    df = pd.DataFrame(columns = ['ID', 'XP', 'Time'])
    df = df.append(data, ignore_index=True)

    print(df)


def del_user():
    return

def edit_user():
    return

def grab_user_info(id):
    df = pd.read_csv("data.csv")

    ids = df["ID"].tolist()

    if id in ids:
        return df["XP"].tolist()[ids.index(id)], df["Time"].tolist()[ids.index(id)]
    
    else:
        add_user(id)
        return False, False


#def loadData()
#def saveData()