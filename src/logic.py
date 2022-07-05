import data_access as da  # data access
import time
from asgiref.sync import async_to_sync
from constants import RANK_DICT


# Check if user is allowed to gain EXP
async def deny_check(user, restrict=None):
    if restrict is None:
        restrict = []
    return True if int(user.id) in restrict or user.bot else await check_time(id)
    

# Check Time
async def check_time(id):
    if not await da.id_exists(id):
        await da.add_user(id)
        return False

    user_xp, user_time, user_lvl = await da.grab_user_info(id)
    return time.time() - int(user_time) <= 60


# Adds rank to user (REQUIRES MEMBER OBJECT NOT JUST ID)
async def promote(member, role: str) -> None:
    await member.add_roles(role)


# Removes rank to user (REQUIRES MEMBER OBJECT NOT JUST ID)
async def demote(member, role: str) -> None:
    await member.remove_roles(role)
    

# Level to a lvl
async def lvl_to(id, lvl):
    user_xp, user_time, user_lvl = await da.grab_user_info(id)
    dlvl = lvl - user_lvl
    await da.add_lvl(id, dlvl)


# Checks rank of user and ranks up (REQUIRES AUTH OBJECT NOT JUST ID)
async def check_rank(auth, member = None) -> tuple[(str / None), bool]:
    user_xp, user_time, user_lvl = await da.grab_user_info(auth.id)

    role_list: list = list(RANK_DICT.keys())

    user_role_list: list = member.roles

    similar_roles: list = list(set(role_list).intersection(set(user_role_list)))

    if not similar_roles:
        return None, False  # returns the highest rank and if they ranked up (str, bool)

    highest_rank: int = -1
    index: int = -1
    for _ in similar_roles:
        rank: int = int((similar_roles[_])[5:6])
        if rank > highest_rank:
            highest_rank = rank
            index = _

    rank: str = similar_roles[index]

    if RANK_DICT[rank] + 1 <= user_lvl:
        index = RANK_DICT[rank].index + 1

        await promote(member, role_list[index])

        return role_list[index], True

    return rank, False
