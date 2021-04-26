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

bot = commands.Bot('>')

@bot.event
async def on_ready():
    print("bot is oPeRAtiOnaL")

@bot.event
async def on_message(message):
    global restrict
    if message.author == bot.user:
        return
    
    #Sets auth as the name of the person in ID form
    auth = message.author.id

    #Check if message sender is allowed to accrue points
    if(lg.deny_check(auth, restrict)):
        return
    
    da.add_xp(auth)

bot.run(config('TOKEN'))