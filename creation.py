# Data Storage
import json

import pandas as pd
from constants import CSV_NAME

df = pd.DataFrame(columns=["ID", "XP", "Time", "Lvl"])
df = df.append({"ID": "330075847799341076", "XP": {"810002138830471178": -1, "gaming": 1, "arts": 1, "fps": 1, "sl": 1, "dnd": 1}, "Time": 100, "Lvl": 0}, ignore_index=True)
df = df.append({"ID": "190625917507207171", "XP": {"810002138830471178": 800, "gaming": 800, "arts": 800, "fps": 800, "sl": 800, "dnd": 1000}, "Time": 101, "Lvl": 11}, ignore_index=True)
df = df.append({"ID": "297540904133197826", "XP": {"810002138830471178": 20, "gaming": 20, "arts": 20, "fps": 20, "sl": 20, "dnd": 3}, "Time": 102, "Lvl": 1}, ignore_index=True)
df = df.append({"ID": "684395467722850345", "XP": {"810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)
df = df.append({"ID": "553441706318626856", "XP": {"810002138830471178": 5, "gaming": 284, "arts": 284, "fps": 284, "sl": 284, "dnd": 284}, "Time": 103, "Lvl": 9}, ignore_index=True)


# print(df)
df.to_csv(CSV_NAME, mode="w", index=False)  # mode="a" for append

df = pd.DataFrame()

df = pd.read_csv("data.csv")

ids = df["ID"].tolist()
xps = df["XP"].tolist()
print(ids)
print(xps)

# Create Restricted List
with open('restricted.json', 'w') as json_file:
    json.dump(["<!@402319880860467201>"],indent = 4,fp=json_file)

# print(df)