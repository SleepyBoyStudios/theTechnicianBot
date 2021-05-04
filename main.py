# for running bot using token see: "bot.run(config('TOKEN'))"
from decouple import config
# For all bot commands used and all data from discord API
from discord.ext import commands
# Import other files
import logic as lg
# Access the user data
import data_access as da

#globals
restrict = []
member = None
auth = None
server = None

bot = commands.Bot('>')  # Initializes bot with '>' prefix


# On bot startup...
@bot.event
async def on_ready():
    print("bot is oPeRAtiOnaL")


# On each message...
@bot.event
async def on_message(message):
    global restrict, auth, member, server
    # Check if the user is the bot or is in the restrict list
    if (message.author == bot.user) or (message.author.id in restrict):
        return

    # Set globals
    member = message
    auth = message.author
    server = message.guild

    # Check if message sender is allowed to accrue points
    if lg.deny_check(auth.id, restrict):
        return
    
    da.add_xp(auth.id)


# ------------------------------------------------------ COMMANDS ------------------------------------------------------

# --------------------------- ADMIN ONLY ---------------------------

#TODO: Adds player to restrict list
@bot.command
async def restrict(auth):
    return


#TODO: Removes player from restrict list
@bot.command
async def unrestrict(auth):
    return


#TODO: Adds xp to a player
@bot.command
async def addXp(auth, amount):
    return


#TODO: Removes xp from a player
@bot.command
async def removeXp(auth, amount):
    return


#TODO: Clears all xp from a player
@bot.command
async def clearXp(auth):
    return


#TODO: Level up player
@bot.command
async def lvlUp(auth):
    return


#TODO: Level down a player
@bot.command
async def lvlDown(auth):
    return


#TODO: Level a player to a rank
@bot.command
async def lvlTo(auth, rank):
    return


#TODO: Prints out the DataFrame
@bot.command
async def df():
    return


#TODO: Prints out the CSV
@bot.command
async def csv():
    return


# --------------------------- GENERAL ---------------------------

# makes sure bot runs with the token from the .env file
bot.run(config('TOKEN'))
