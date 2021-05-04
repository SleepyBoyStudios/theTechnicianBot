import data_access as da  # data access API
import time
from constants import RANK_DICT

# Check if user is allowed to gain EXP
def deny_check(auth, restrict):
    if auth in restrict:
        return True
    else:
        return check_time(auth)


# Check Time
def check_time(auth):
    if not da.id_exists(auth):
        da.add_user(auth)
        return False

    user_xp, user_time, user_lvl = da.grab_user_info(auth)
    if time.time() - int(user_time) <= 60:
        return True
    else:
        return False


#Checks rank of user and ranks up
def check_rank(auth):
    user_xp, user_time, user_lvl = da.grab_user_info(auth)

    role_list = list(RANK_DICT.keys())

    user_role_list = auth.member.roles

    similar_roles = list(set(role_list).intersection(set(user_role_list)))
    
    if similar_roles != []:
        highest_rank = 0
        index = 0
        for _ in similar_roles:
            rank = int((similar_roles[_])[5:6])
            if rank > highest_rank:
                highest_rank = int((similar_roles[_])[5:6])
                index = _

    else:
        return 0, False

    rank = similar_roles[index]

    if RANK_DICT[rank] <= user_xp:
        index = RANK_DICT[rank].index
        promote(auth, role_list[index+1])
        return highest_rank, True
    
    return highest_rank, False



#TODO: Adds rank to user
def promote(auth, role):
    return


#TODO: Removes rank to user
def demote():
    return
