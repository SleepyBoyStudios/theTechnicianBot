DB
    User_Info
        : user_ID - PK
        : total_XP
        : level
        : time
        : is_restricted
    Server_1 - guild (server) ID
        : server_1_Rec_ID - PK
        : user_ID - FK -> User_Info.userID
        : server_XP
    Server_2 - guild (server) ID
        : server_2_Rec_ID - PK
        : user_ID - FK -> User_Info.userID
        : server_XP

    ...

    Server_n - guild (server) ID
        : server_n_Rec_ID - PK
        : user_ID - FK -> User_Info.userID
        : server_XP
