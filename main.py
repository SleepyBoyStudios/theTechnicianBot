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

bot = commands.Bot('>')

@bot.event
async def on_ready():
    id = 684395467722850345
    xp, time = da.grab_user_info(id)
    if xp is type(int):
        add_xp(id)
    print(xp, time)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return



bot.run(config('TOKEN'))