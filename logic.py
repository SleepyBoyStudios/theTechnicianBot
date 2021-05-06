import data_access as da  # data access API
import time
from constants import RANK_DICT

# Check if user is allowed to gain EXP
def deny_check(id, restrict):
    if int(id) in restrict:
        return True
    else:
        return check_time(id)


# Check Time
def check_time(id):
    if not da.id_exists(id):
        da.add_user(id)
        return False

    user_xp, user_time, user_lvl = da.grab_user_info(id)
    if time.time() - int(user_time) <= 60:
        return True
    else:
        return False


#TODO: Level to a lvl
def lvl_to(id, lvl):
    return


# Checks rank of user and ranks up (REQUIRES AUTH OBJECT NOT JUST ID)
def check_rank(auth, member=None):
    user_xp, user_time, user_lvl = da.grab_user_info(auth.id)

    role_list = list(RANK_DICT.keys())

    user_role_list = member.roles

    similar_roles = list(set(role_list).intersection(set(user_role_list)))
    
    if similar_roles != []:
        highest_rank = -1
        index = -1
        for _ in similar_roles:
            rank = int((similar_roles[_])[5:6])
            if rank > highest_rank:
                highest_rank = rank
                index = _

    else:
        return None, False # returns the highest rank and if they ranked up (str, bool)

    rank = similar_roles[index]

    if RANK_DICT[rank] + 1 <= user_lvl:
        index = RANK_DICT[rank].index + 1

        promote(member, role_list[index])

        return role_list[index], True
    
    return rank, False


# Adds rank to user (REQUIRES MEMBER OBJECT NOT JUST ID)
def promote(member, role):
    member.add_roles(str(role))


# Removes rank to user (REQUIRES MEMBER OBJECT NOT JUST ID)
def demote(member, role):
    member.remove_roles(str(role))
