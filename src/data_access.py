# Data Storage
import pandas as pd  # Database Library
from constants import DB_PATH, CSV_NAME, LVL_LIST_PATH  # Imports constants from 'constants.py'
import random as rd  # Random Library
import time  # Time Library
import json  # conversion of string to dict
import sqlalchemy as sa # Database engine

# Loads table from database
def load_table(tbl: str = None) -> (Exception / pd.DataFrame):
    raise Exception('No table to load DataFrame from') if tbl is None else pd.read_sql_table(tbl, sa.create_engine(f'sqlite://{DB_PATH}'))


# Saves to CSV
def save_data(new_df: pd.DataFrame, m: str = 'w'):
    new_df.to_csv(CSV_NAME, mode=m, index=False)


# Saves table from database
def save_table(new_df: pd.DataFrame, tbl: str = None) -> (Exception / None):
    # sourcery skip: raise-specific-error
    if tbl is None: raise Exception('No table to save DataFrame in')
    engine = sa.create_engine(f'sqlite://{DB_PATH}')
    with engine.begin():
        new_df.to_sql(tbl, engine, if_exists='replace')


# Loads levels from CSV
def load_lvls() -> pd.DataFrame:
    return pd.read_csv(LVL_LIST_PATH, sep=',', header=None)


def grab_restricted_list() -> list:
    with open('restricted.json') as file:
        return json.load(file)


def store_restricted_list(list: list):
    with open('restricted.json','w') as file:
        json.dump(list, indent=4, fp=file)



async def get_network_table(network_id: int = 0) -> list: #! for future use
    engine = sa.create_engine(f'sqlite://{DB_PATH}')
    return engine.execute(f'SELECT * FROM Network_{network_id}').fetchall()



async def get_table_names() -> list:
    inspector = sa.inspect(sa.create_engine(f'sqlite://{DB_PATH}'))
    return inspector.get_table_names()


# Globals
df_user_info = load_table(tbl='user_info')
lvls = load_lvls()
engine = sa.create_engine(f'sqlite://{DB_PATH}')
network_tables = get_table_names()
# network_table_list = get_network_tables() #! for future use


# returns dataframe
def load_dataframe():
    return df


# Sets the time in the DataFrame
async def __set_time(user_time) -> int:
    global df
    df['Time'] = df['Time'].replace(to_replace=user_time, value=int(time.time()))


# Checks if the id {user_id} exists
async def id_exists(user_id) -> (int / bool):
    global df_user_info

    user = df_user_info.loc(await df_user_info.index(user_id))  # gets id index from DataFrame and stores it in the variable 'id_index'

    # If length of the id != 0 (df.loc() is to locate)
    return user if len(user) != 0 else False


# Adds user to the DataFrame and to the database
async def add_user(user_id: int) -> None:
    global df_user_info
    data = {'user_ID': user_id, 'total_XP': 0, 'level': 0, 'time': 0} # Temporary 1 item DataFrame stored in 'data'

    print(f'\n{data}\n')

    df_user_info = df_user_info.append(data, ignore_index=True)  # append temp DataFrame to global DataFrame
    df_user_info = df_user_info.head()

    print(f'{df_user_info.head()}\n')

    # update database
    print(f'Adding user: {user_id}... ')

    try:
        await save_table(new_df=df_user_info, tbl='User_Info')
    except Exception as e:
        raise f'Error adding user, thrown:\n{e}' from e
    print('Done!\n')


# Deletes a user from the DataFrame and CSV
async def del_user(id: int) -> None:
    global df_user_info

    df_user_info = df_user_info.set_index('user_ID')  # Sets the Index as the ID variable
    df_user_info = df_user_info.head()
    df_user_info = df_user_info.drop(id)  # Drops the row containing the id in 'id'

    print(f'Dropping id: {id}... ')
    try:
        await save_table(new_df=df_user_info, tbl='User_Info')
    except Exception as e:
        raise f'Error deleting user, thrown: \n {e}' from e
    print('Done!\n')


# move if statement to logic.py and keep XP update here
async def add_xp(id: int, server: int, amount: int = 0) -> None:
    user_xp, user_time, user_lvl = await grab_user_info(id) # Gets user xp, time, and level

    xp = user_xp.copy()
    xp[server] = user_xp.get(server) + amount if amount != 0 else rd.randint(25, 50)

    xp_df = await load_table(server)

    xp_df.update(xp)

    try:
        await save_table(pd.from_dict(xp_df), tbl=f'{server}')
    except Exception as e:
        raise e
    await __set_time(user_time)

    # Update CSV
    print('xp added')


# level upgrading
async def add_lvl(id: int, amount: int = 1) -> None:
    global df_user_info, lvls

    user_xp, user_time, user_lvl = await grab_user_info(id)

    lvl: int = user_lvl + amount
    df_user_info['level'] = df_user_info['level'].replace(to_replace=user_lvl, value=lvl)

    lvl_xp: int = int(lvls.loc[lvl + 1, 0].split(',')[1])

    servers: list = user_xp.keys()

    lvl_xp -= sum(user_xp.values())

    for _ in servers:
        x = lvl_xp // len(servers)
        add_xp(id, _, x)

    if lvl_xp % len(servers) != 0:
        mod_amount = lvl_xp % len(servers)
        for _ in range(mod_amount):
            add_xp(id, servers, 1)

    await __set_time(user_time)
   
    try:
        await save_table(df_user_info, 'User_Info')
    except Exception as e:
        raise e
    print('Level added and saved')


async def remove_lvl(user_id, amount) -> None:
    global df_user_info, lvls

    user_xp, user_time, user_lvl = await grab_user_info(user_id)

    lvl: int = user_lvl - amount
    xp: int = lvls.loc[lvl]
    df_user_info['level'] = await df_user_info['level'].replace(to_replace=user_lvl, value=lvl)
    df_user_info['total_xp'] = await df_user_info['total_xp'].replace(to_replace=user_xp, value=xp)

    await __set_time(user_time)
   
    try:
        await save_data(df_user_info, 'User_Info')
    except Exception as e:
        raise e
    print('Level removed and saved')


# clear all levels (including xp)
async def clear_lvl(id) -> None:
    global df

    user_xp, user_time, user_lvl = await grab_user_info(id)

    lvl = 0
    df['Lvl'] = df['Lvl'].replace(to_replace=user_lvl, value=lvl)

    xp = await user_xp.fromkeys(user_xp.iterkeys(), 0)
    df['XP'] = df['XP'].replace(to_replace=user_xp, value=xp)

    await __set_time(user_time)

    print('Level added and saved')
    await save_data(df)


# Gets the user's info (xp, time, & level)
async def grab_user_info(user: int) -> tuple(dict, int, int):
    global df_user_info, network_tables

    ids: list = df_user_info['user_ID'].tolist() # Gets a list of all the ids in the DataFrame
    
    select_str: str = ''
    join_str: str = ''
    for _ in range(len(network_tables) - 2):
        select_str += f'{network_tables[_]}.server_xp AS {network_tables[_]}_xp, ' # Selects server_xp and aliases then to the server their xp is stored in
        join_str += f'INNER JOIN {network_tables[_]} ON {network_tables[_]}.user_ID = User_Info.user_ID' # Joins all tables in the network together

    # Check query in terminal
    print(f'\nSELECT {select_str} FROM User_Info {join_str} WHERE User_Info.user_ID = {user}\n')
    
    # Runs query and stores it in a DataFrame
    user_server_xp: pd.DataFrame = pd.read_sql_query(f'SELECT {select_str} FROM User_Info {join_str} WHERE User_Info.user_ID = {user}')

    print(f'grabbed info:\n{user_server_xp}')

    user_server_xp = user_server_xp.set_index('user_ID')
    user_server_xp = user_server_xp.to_dict()
    return user_server_xp, df_user_info['time'].tolist()[ids.index(user)], df_user_info['level'].tolist()[ids.index(user)]
