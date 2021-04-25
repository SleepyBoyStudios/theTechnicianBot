


#Event that happens when a message is sent
@bot.event
async def on_message(message):
    global auth, members, increment

    #Sets auth as the name of the person (DrDev#9289) as opposed to the object that message.author is
    auth = str(message.author)
    print(auth)
    #Searches the members array, and if the author in one of the kinder objects, stops method.
    print("here")
    print(members)
    for kind in members:
        print(kind.get_id())
        print(auth)
        if kind.get_id() is auth:
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