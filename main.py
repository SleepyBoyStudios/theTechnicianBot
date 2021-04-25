#————————————————————————————————————————LIBRARIES————————————————————————————————————————
#for asynchronous actions (async def ...)
import asyncio
#discord API
import discord
#line buffer for file reading
import linecache as ln
#for handling multiple threads
import threading
#for getting the time of a user's actions
import time
#random class
import random as rd
#for running bot using token see: "bot.run(config('TOKEN'))"
from decouple import config
#For all bot commands used and all data from discord API
from discord.ext import commands
#Data Storage
import pandas as pd
#Import other files
from logic import check_time

#
#————————————————————————————————————————GLOBAL VARIABLES————————————————————————————————————————
#

restrict = ['TheTechnician#2981', 'C.J.#8161']

#Setting Prefix as >
bot = commands.Bot('>')

#ranks which have the privilage to be another role
roleRanks = [5, 10, 20, 30, 40, 50, 60, 70]

#Current row after update stats
row = -1

#point increment
increment = 0

#cooldown between adding points
cooldown = 60

#
#————————————————————————————————————————INITIALIZATION————————————————————————————————————————
#

#Event that happens on initialization of bot
@bot.event
async def on_ready():
    global roleRanks
    #Prints to console that bot has logged in
    print('We have logged in as {0.user}'.format(bot))

bot.run(config('TOKEN'))


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
    
#Class that defines the leveling for current level and if the author has level
class level:

    def __init__(self, auth, xp, bot):
        self.auth = auth
        self.xp = int(xp)
        self.level= 0
        self.ref = 'levelVals.txt'
        self.bot = bot

    def get_level(self):
        global ws, row
        currentRank = self.get_orig_level()

        if currentRank == 0:
            for i in self.auth.roles:
                if 'Rank' in str(i.name):
                    currentRank = int(i.name[(' ')+1:(':')])
                while int(ln.getline(self.ref, currentRank+1)) <= self.xp:
                    currentRank+=1
        else:
            currentRank = int(currentRank)

        return currentRank

    def get_orig_level(self):
        orig = ws.cell(row, ws.row_values(1).index('Rank')+1).value
        if orig is None:
            return 0
        return int(orig)

    def has_leveled(self):
        nextLevelXP = int(ln.getline(self.ref, self.get_orig_level()+1))
        if nextLevelXP <= self.xp:
            return True
        return False

    def __str__(self):
        print(str(self.auth) +" "+ str(self.get_level()))

