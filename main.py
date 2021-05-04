import asyncio
#discord API
import discord
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
import logic as lg
#Access the user data
import dataAccess as da
import time

restrict = []

bot = commands.Bot('>') #Initializes bot with '>' prefix


#On bot startup...
@bot.event
async def on_ready():
    print("bot is oPeRAtiOnaL")


#On each message...
@bot.event
async def on_message(message):
    global restrict
    if (message.author == bot.user) or (message.author in restrict): #Check if the user is the bot or is in the restrict list 
        return
    
    #Sets auth as the name of the person in ID form
    auth = message.author.id

    #Check if message sender is allowed to accrue points
    if(lg.deny_check(auth, restrict)):
        return
    
    da.add_xp(auth)

#-------------------------------------------------------------------------- COMMANDS --------------------------------------------------------------------------

#--------------------------- ADMIN ONLY ---------------------------

#Adds player to restrict list
@bot.command
async def restrict(auth):
    return


#Removes player from restrict list
@bot.command
async def unrestrict(auth):
    return


#Adds xp to a player
@bot.command
async def addXp(auth):
    return


#Removes xp from a player
@bot.command
async def removeXp(auth):
    return


#Level up player
@bot.command
async def lvlUp(auth):
    return


#Level down a player
@bot.command
async def lvlDown(auth):
    return


#Level a player to a rank
@bot.command
async def lvlTo(auth, rank):
    return


#Prints out the DataFrame
@bot.command
async def df():
    return


#Prints out the CSV
@bot.command
async def csv():
    return

#--------------------------- GENERAL ---------------------------

#makes sure bot runs with the token from the .env file
bot.run(config('TOKEN'))