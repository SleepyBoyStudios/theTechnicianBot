import data_access as da  # data access API
import time


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
