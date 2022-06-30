# Data Storage
import sqlite3 as db
import sqlalchemy as sa
import pandas as pd
import sys

sys.path.append('.')

from src.constants import DB_PATH

alc = sa.create_engine(rf"sqlite://{DB_PATH}").connect()
script = db.connect(rf".{DB_PATH}")

sql_create_script = open(r"./Testing/Queries/create_database.sql").read()
sql_drop_script = open(r"./Testing/Queries/drop_db.sql").read()

if (script.execute('SELECT * FROM sqlite_master').fetchall()):
    script.executescript(sql_drop_script)

script.executescript(sql_create_script)

# ---------------------------------------------------------------

with alc.begin():

# ---------------------------------------------------------------

    with alc.begin_nested():

        df = pd.read_csv(r"./Testing/TestDataCSV/User_info.csv")

        print(f'DataFrame: {type(df["user_ID"][0])}\nin transaction: {alc.in_transaction}')

        df.to_sql(name='User_Info',
                con=alc,
                if_exists='append',
                index=False) 

    # ---------------------------------------------------------------

    with alc.begin_nested():

        df = pd.read_csv(r"./Testing/TestDataCSV/server_1.csv")

        print(f'in transaction: {alc.in_transaction}\n')

        df.to_sql(name='Server_991178883682541700',
                con=alc,
                if_exists='append',
                index=False)

    # ---------------------------------------------------------------

    with alc.begin_nested():

        df = pd.read_csv(r"./Testing/TestDataCSV/server_2.csv")

        print(f'in transaction: {alc.in_transaction}\n')

        df.to_sql(name='Server_810002138830471178',
                con=alc,
                if_exists='append',
                index=False)


# ---------------------------------------------------------------

user_info = server_1 = server_2 = pd.DataFrame()

user_info = pd.read_sql_table('User_Info', alc)
server_1 = pd.read_sql_table('Server_991178883682541700', alc)
server_2 = pd.read_sql_table('Server_810002138830471178', alc)

alc.close()
script.close()

print(f'Sample database created:\n{user_info.head()}\n\n {server_1.head()}\n\n {server_2.head()}\n')
