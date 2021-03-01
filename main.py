#————————————————————————————————————————LIBRARIES————————————————————————————————————————
#for asynchronous actions (async def ...)
import asyncio
#Interface with google sheets API
import gspread
#line buffer for file reading
import linecache as ln
#for handling multiple threads
import threading
#for getting the time of a user's actions
import time
#for running bot using token see: "bot.run(config('TOKEN'))"
from decouple import config
#For all bot commands used and all data from discord API
from discord.ext import commands

#
#————————————————————————————————————————GLOBAL VARIABLES————————————————————————————————————————
#

#Prefix for commands in discord
pre = '>'

#Setting Prefix as pre
bot = commands.Bot(pre)

#Current Author of a Message Being Processed
auth = ''

#Google Sheets Worksheet Being Used for Point Storage
ws = None

#List of members who have spoken in the last minute, for "spam" protection
members = []

#Exp of Selected Author
exp = None

#Current row after update stats
row = -1

#
#————————————————————————————————————————CLASSES————————————————————————————————————————
#

#Class that defines a human, and the time of their last message. Used in "spam" protection.
class kinder:
    def __init__(self, id): 
        self.id = id
        self.zeit = int(time.time())
        
    def get_id(self):
        return self.id
        
    def get_time(self):
        return self.zeit

    def __str__(self):
        return 'The user, ' + self.id + 'is on cooldown from' + self.zeit
    

class level:

    def __init__(self, auth, xp, bot):
        self.auth = auth
        self.xp = xp
        self.level= 0
        self.ref = 'levelVals.txt'
        self.bot = bot
        
    def get_level(self):
        currentRank = 0

        return currentRank

    def has_leveled(self):
        if ln.getline('levelVals.txt', self.get_level()+1) <= self.xp:
            return True
        return False

    def __str__(self):
        print(str(self.auth) +" "+ str(self.get_level()))

#
#————————————————————————————————————————BOT-EVENT METHODS————————————————————————————————————————
#

#Event that happens on initialization of bot
@bot.event
async def on_ready():
    global ws, members
    #Prints to console that bot has logged in
    print('We have logged in as {0.user}'.format(bot))

    #Starts the second thread for checking cooldowns
    await start_thread()

    #Sets the database to the specified worksheet using the key
    ws = gspread.service_account('keyFile.json').open('Level Bot').get_worksheet(0)


#Event that happens when a message is sent
@bot.event
async def on_message(message):
    global auth, members, exp
    #Searches the members array, and if the author in one of the kinder objects, stops method.
    for kind in members:
        if kind.get_id() is auth:
            return
    
    #Makes sure the bot can't give itself points
    if not str(message.author) in 'TheTechnician#2981':
        #Sets auth as the name of the person (DrDev#9289) as opposed to the object that message.author is
        auth = str(message.author)

        #Console recognition of adding one point to user auth's exp
        print(f'added 1 point to {auth}\n')

        #Discord recognition of adding one point to user auth's exp
        await message.channel.send(f"one point added for {auth}")

        #Creates a kinder object to add to members list, with the user's name. "spam" protection.
        members.append(kinder(auth))

        #See corresponding method
        await update_stats()

        

    await bot.process_commands(message)

#Event that happens when the prefix is used, here, in addition to the word 'say'
@bot.command()
async def say(ctx, *, par):
    global auth
    try:
        #Tries to send a message with the user's entered data, followed by a @ for the user that used the command
        await ctx.send(f'{par}, {ctx.author.mention}')

    except Exception:
        #When the user only enters '>say' with no other data
        await ctx.send(f'{ctx.author.mention}')
    
    #Console confirmation of this command working
    print(f'{auth} told TheTechnician to say {par}\n')


#
#————————————————————————————————————————HELPER METHODS————————————————————————————————————————
#


#Helper method for starting the secondary thread
async def start_thread():
    #literally just runs the next method lol
    th = threading.Thread(target=asyncio.run, args=(check_time(),))
    th.start()


#This is the loop running in the second thread
async def check_time():
    global members
    #Quality loop, I know
    while(True):
        #Checks all the objects in members list and if their time (in seconds) from creation is over 60, they're popped off the list.
        for kind in members:
            if (int(time.time()) - kind.get_time()) > 60:
                members.pop()
        #Check every second (sleeps for one second)
        time.sleep(1)

#Interface exp with google sheets
async def update_stats():
    #Pay attention, you bot.
    await bot.wait_until_ready()
    global auth, ws, exp, row
    
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
    cell_list = ws.findall(auth)

    #If there are no entries, time to create a row for the ~new~ user
    if len(cell_list) == 0:
        #Find the number of exising rows that correspond to humans
        numPeople = len(ws.col_values(1))
        #Set row
        row = numPeople+1
        #Create the row for that user
        ws.update_cell(row, 1, auth)
        #Add the inital value for sending their first message, 25 exp
        ws.update_cell(row, column, '25')
    else:
        #Grabs the location of the player's row. If done right, player never has more than one entry in the list
        row = cell_list[0].row
        try:
            #Grabs value already in cell, and adds 25 to it.
            newVal = int(ws.cell(row, column).value)+25
        except Exception:
            #If no value in cell, the new value is 25 (one message)
            newVal = 25
        
        #Update exp to newVal in server, denoted by column, for user, denoted by row
        ws.update_cell(row, column, newVal)

        #levelCheck = level(message.author, exp, message)
        #if levelCheck.has_leveled():
        #    if(level.get_level() > )


'''
@bot.command()
async def clearStats(ctx):
    with open("stats.txt", 'w') as f:
        f.write("")
    await ctx.send("Cleared stats.txt!!")
    print('stats cleared\n')


@bot.command()
async def stats(ctx):
    with open("stats.txt", 'r') as f:
        cont=f.read()
    
    try:	
        await ctx.send(cont)
        print('stats printed\n')

    except Exception:
        await ctx.send('`NO STATS PRESENT`')
        print('no stats\n')
'''

#
#————————————————————————————————————————INITIALIZATION————————————————————————————————————————
#

bot.run(config('TOKEN'))