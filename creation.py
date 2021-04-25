#Data Storage
import pandas as pd

df=pd.DataFrame(columns = ['Name', 'XP', 'Time'])
df = df.append({"Name" : "CJ", "XP" : "-1", "Time" : "100"}, ignore_index=True)
df = df.append({"Name" : "Lux", "XP" : "5000", "Time" : "101"}, ignore_index=True)
df = df.append({"Name" : "Dev", "XP" : "123", "Time" : "102"}, ignore_index=True)
df = df.append({"Name" : "QVint", "XP" : "3425", "Time" : "103"}, ignore_index=True)

df.to_csv('data.csv',mode='w',index=False) #mode='a' for append

df=pd.DataFrame()

df=pd.read_csv('data.csv')

print(df)