# for running bot using token see: "bot.run(config('TOKEN'))"
from decouple import config
# For all bot commands used and all data from discord API
from discord.ext import commands
# Import other files
import logic as lg
# Access the user data
import data_access as da
import re

# Import constants


bot = commands.Bot('>')  # Initializes bot with '>' prefix


# -------------------------------------------------- BUILT IN METHODS --------------------------------------------------

# On bot startup...
@bot.event
async def on_ready():
    print("bot is oPeRAtiOnaL")


# On each message...
@bot.event
async def on_message(message):
    # Set locals
    restrict = da.grab_restricted_list()
    # member = await bot.fetch_user(message.author.id)
    auth = message.author
    server = message.guild.id

    # Check if message sender is allowed to accrue points
    if lg.deny_check(auth, restrict):
        return

    da.add_xp(auth.id, server)

    await bot.process_commands(message)


# ------------------------------------------------------ COMMANDS ------------------------------------------------------

# --------------------------- ADMIN ONLY ---------------------------

# Adds player to restrict list
@bot.command(pass_context=True)
async def rest(ctx, user):
    restrict = da.grab_restricted_list()
    if user in restrict:
        await ctx.send("The user, " + user + " is already restricted!")
    else:
        restrict.append(user)
        da.store_restricted_list(restrict)
        await ctx.send("The user, " + user + " has been added to the restriction list.")


# Removes player from restrict list
@bot.command(pass_context=True)
async def unrestrict(ctx, user):
    restrict = da.grab_restricted_list()
    try:
        restrict.remove(user)
        da.store_restricted_list(restrict)
        await ctx.send("Removed " + user + " from the restriction list!")
    except ValueError:
        await ctx.send("That user is already not on the restricted list!")


# TODO: Adds xp to a player
@bot.command
async def addXp(user, amount):
    da.add_xp(amount)


# TODO: Removes xp from a player
@bot.command
async def removeXp(user, amount):
    da.add_xp(-amount)


# TODO: Clears all xp from a player
@bot.command
async def clearXp(user):
    da.clear_lvl(user)


# TODO: Level up player
@bot.command(pass_context=True)
async def lvlUp(ctx, user, amount=1):  # user id format '<!@3892472389468912>'
    user = re.sub('[^0-9]+', '', user)
    da.add_lvl(user, amount)


# TODO: Level down a player
@bot.command
async def lvlDown(user):
    da.remove_lvl()


# TODO: Level a player to a lvl
@bot.command
async def lvlTo(user, lvl):
    lg.lvl_to(user, lvl)


# TODO: Prints out the DataFrame
@bot.command
async def df():
    return da.load_dataframe()


# TODO: Prints out the CSV
@bot.command
async def csv():
    return da.load_data()


# ------------------------------------------------------ BOT SETUP -----------------------------------------------------

# makes sure bot runs with the token from the .env file
bot.run(config('TOKEN'))
