#Data Storage
import pandas as pd
import constants as const

df=pd.DataFrame(columns = ['ID', 'XP', 'Time'])
df = df.append({"ID" : 330075847799341076, "XP" : -1, "Time" : 100}, ignore_index=True)
df = df.append({"ID" : 190625917507207171, "XP" : 5000, "Time" : 101}, ignore_index=True)
df = df.append({"ID" : 297540904133197826, "XP" : 123, "Time" : 102}, ignore_index=True)
df = df.append({"ID" : 684395467722850345, "XP" : 3425, "Time" : 103}, ignore_index=True)

#print(df)

df.to_csv(const.CSV_NAME,mode='w', index=False) #mode='a' for append

df=pd.DataFrame()

df=pd.read_csv('data.csv')

ids = df["ID"].tolist()
xps = df["XP"].tolist()
print(ids)
print(xps)

#print(df)