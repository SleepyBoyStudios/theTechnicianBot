# for running bot using token see: "bot.run(config('TOKEN'))"
from decouple import config
# import discord API
import discord
# For all bot commands used and all data from discord API
from discord.ext import commands
# Import other files
import logic as lg
# Access the user data
import data_access as da
# Import constants


#globals
restrict = []
member = None
auth = None
server = None

bot = commands.Bot('>')  # Initializes bot with '>' prefix

# ------------------------------------------------------ BUILT IN METHODS ------------------------------------------------------

# On bot startup...
@bot.event
async def on_ready():
    print("bot is oPeRAtiOnaL")


# On each message...
@bot.event
async def on_message(message):
    global restrict, auth, member, server


    #if message.bot:
    #    return

    #TODO: Check if the user is the bot or is in the restrict list BROKEN
    #if (message.author.id == bot.user.id) or (message.author.id in restrict):
    #    return
    # Set globals
    member = await bot.fetch_user(message.author.id)
    auth = message.author
    server = message.guild.id
    print(type(server))

    # Check if message sender is allowed to accrue points
    #if lg.deny_check(auth.id, restrict):
    #    return
    
    da.add_xp(auth.id, server)
    da.add_lvl(auth.id, 1)


# ------------------------------------------------------ COMMANDS ------------------------------------------------------

# --------------------------- ADMIN ONLY ---------------------------

#TODO: Adds player to restrict list
@bot.command
async def rest(user):
    restrict.push(user)


#TODO: Removes player from restrict list
@bot.command
async def unrestrict(user):
    restrict.pop(user)


#TODO: Adds xp to a player
@bot.command
async def addXp(user, amount):
    da.add_xp(amount)


#TODO: Removes xp from a player
@bot.command
async def removeXp(user, amount):
    da.add_xp(-amount)


#TODO: Clears all xp from a player
@bot.command
async def clearXp(user):
    da.clear_lvl(user)


#TODO: Level up player
@bot.command
async def lvlUp(user):
    da.add_lvl(user)


#TODO: Level down a player
@bot.command
async def lvlDown(user):
    da.remove_lvl()


#TODO: Level a player to a lvl
@bot.command
async def lvlTo(user, lvl):
    lg.lvl_to(user, lvl)


#TODO: Prints out the DataFrame
@bot.command
async def df():
    return da.load_dataframe()


#TODO: Prints out the CSV
@bot.command
async def csv():
    return da.load_data()


# --------------------------- GENERAL ---------------------------



# ------------------------------------------------------ BOT SETUP ------------------------------------------------------

# makes sure bot runs with the token from the .env file
bot.run(config('TOKEN'))
