#Data Storage
import pandas as pd
from constants import CSV_NAME

#constants

def add_user(id):
    data = {"ID": id, "XP": 0, "Time": 0}
    #make temporary DataFrame
    df = pd.DataFrame(columns = ['ID', 'XP', 'Time'])
    df = df.append(data, ignore_index=True)

    print(df)
    #update csv file
    df.to_csv(CSV_NAME, mode='a', index=False)

def del_user(id):
    df = pd.read_csv(CSV_NAME)

    df = df.set_index("ID")
    df.head()

    df = df.drop(id)
    print(df)

    print("Dropping id: " + str(id) + "...")
    df.to_csv(CSV_NAME, mode='w', index=False)
    print("Done!\n")



def edit_user():
    return

def add_xp(id):
    ids = pd.read_csv(CSV_NAME)["ID"].tolist()
    if id in ids:
        #Add xp
        return
    
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


#def loadData()
#def saveData()