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
import logic as log

#
#————————————————————————————————————————CLASSES————————————————————————————————————————
#

#Class that defines a human, and the time of their last message. Used in "spam" protection.
#class kinder:
#    def __init__(self, id): 
#        self.id = id
#        self.zeit = int(time.time())
#        
#    def get_id(self):
#        return self.id
#        
#    def get_time(self):
#        return self.zeit
#
#    def __str__(self):
#        return 'The user, ' + self.id + 'is on cooldown from' + self.zeit
    
#Class that defines the leveling for current level and if the author has level
#class level:
#
#    def __init__(self, auth, xp, bot):
#        self.auth = auth
#        self.xp = int(xp)
#        self.level= 0
#        self.ref = 'levelVals.txt'
#        self.bot = bot
#
#    def get_level(self):
#        global ws, row
#        currentRank = self.get_orig_level()
#
#        if currentRank == 0:
#            for i in self.auth.roles:
#                if 'Rank' in str(i.name):
#                    currentRank = int(i.name[(' ')+1:(':')])
#                while int(ln.getline(self.ref, currentRank+1)) <= self.xp:
#                    currentRank+=1
#        else:
#            currentRank = int(currentRank)
#
#        return currentRank
#
#    def get_orig_level(self):
#        orig = ws.cell(row, ws.row_values(1).index('Rank')+1).value
#        if orig is None:
#            return 0
#        return int(orig)
#
#    def has_leveled(self):
#        nextLevelXP = int(ln.getline(self.ref, self.get_orig_level()+1))
#        if nextLevelXP <= self.xp:
#            return True
#        return False
#
#    def __str__(self):
#        print(str(self.auth) +" "+ str(self.get_level()))


#
#————————————————————————————————————————GLOBAL VARIABLES————————————————————————————————————————
#

restrict = ['TheTechnician#2981', 'C.J.#8161']

#ranks which have the priveledge to be another role
roleRanks = [5, 10, 20, 30, 40, 50, 60, 70]

#Current row after update stats
row = -1

#point increment
increment = 0

#cooldown between adding points
cooldown = 60

#
#————————————————————————————————————————BOT EVENTS————————————————————————————————————————
#
#Setting Prefix as >
bot = commands.Bot('>')

#Event that happens on initialization of bot
@bot.event
async def on_ready():
    global roleRanks
    #Prints to console that bot has logged in
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    #global auth, members, increment

    #Sets auth as the name of the person (DrDev#9289) as opposed to the object that message.author is
    auth = str(message.author)
    #Searches the members array, and if the author in one of the kinder objects, stops method.
    if(log.denyCheck(auth)):
        return
    
    #Makes sure the bot can't give itself points
    if not str(message.author) in restrict:
        
        #randomizes increment on every message
        increment = rd.randint(25, 50)

        #Console recognition of adding one point to user auth's exp
        print(f'added {increment} points to {auth}\n')

        #Discord recognition of adding one point to user auth's exp
        await message.channel.send(f"{increment} points added for {auth}")

        #Creates a kinder object to add to members list, with the user's name. "spam" protection.
        members.append(kinder(auth))

        #See corresponding method
        await update_stats(False, auth)

    await bot.process_commands(message)


@bot.event
async def on_member_remove(ctx):
   await update_stats(True, ctx)


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


bot.run(config('TOKEN'))