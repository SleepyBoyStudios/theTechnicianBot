import dataAccess as dA

#Check if user is allowed to gain EXP
def deny_check(auth, restrict):
    if auth in restrict:
        return True
    else:
        return check_time(auth)

#This is the loop running in the second thread
async def check_time(auth):
    userData = dA.grabUser(auth)



#Interface exp with google sheets
async def update_stats(clear, auth):
    #Pay attention, you bot.
    await bot.wait_until_ready()
    global ws, row, roleRanks, increment
    
    #Find the name of the server the bot is in.
    serverName = bot.guilds[0].name
    
    #Grabs the list of column names.
    serversList = ws.row_values(1)

    #Finds the correct column for this server, to input the exp for the user
    for val in serversList:
        if val in serverName:
            column = serversList.index(val)+1
            break

    #Finds the row that the author of the message is in. Returns list
    cell_list = ws.findall(str(auth))

    #If there are no entries, time to create a row for the ~new~ user
    if len(cell_list) == 0:
        #Find the number of exising rows that correspond to humans
        numPeople = len(ws.col_values(1))
        #Set row
        row = numPeople+1
        #Create the row for that user
        ws.update_cell(row, 1, str(auth))
        #Add the inital value for sending their first message, {increment} exp
        ws.update_cell(row, column, f'{increment}')
    else:
        #Grabs the location of the player's row. If done right, player never has more than one entry in the list
        row = cell_list[0].row
        if clear == False:
            try:
                #Grabs value already in cell, and adds {increment} to it.
                newVal = int(ws.cell(row, column).value)+increment
            except Exception:
                #If no value in cell, the new value is {increment} (one message)
                newVal = increment
        else:
            newVal = 0
            
        #Update exp to newVal in server, denoted by column, for user, denoted by row
        ws.update_cell(row, column, newVal)
        if clear == True:
            delCheck(row)

    #gets the value of the player's total xp
    col = ws.row_values(1).index('TOTALEN')+1
    #instantiated the level object and strores it in levelCheck
    levelCheck = level(auth, ws.cell(row, col).value, bot)
    #checks if teh player has leveled
    if levelCheck.has_leveled():
        #if the player hasn leveled, it updates the rank in the excel sheet
        ws.update_cell(row, ws.row_values(1).index('Rank')+1, levelCheck.get_level())
        #checks if new rank obtains a ~fancy~ role
        if levelCheck.get_level() in roleRanks:
            #if so, calls add_rank_role() function
            await add_rank_role(levelCheck.get_level(), auth)


#get's the point list from sheet
async def delCheck(row):
    pointList = ws.row_values(row)
    

#adds role 'Rank [num]: {name}' to player
async def add_rank_role(rank, auth):
    global bot

    #stores rank name in roleRank & get's all roles in a guild(server)
    roleName = f'Rank {rank}'
    guildRoles = bot.guilds[0].roles

    #iterates through the roles
    for role in guildRoles:
        #checks if the role exists
        if roleName in role.name:
            #adds player to role
            await auth.add_roles(role, atomic=True)

            #if role does not exist, checks if it is the last role of the list
        elif guildRoles.index(role) == (len(guildRoles)-1):
            await bot.create_role(auth.server, name=roleName)
            await auth.add_roles(roles= roleName, atomic=True)