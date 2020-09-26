import discord
from discord.ext import commands
import os
import string


bot=commands.Bot(command_prefix='/')


@bot.event
async def on_member_join(member):
    print(f'{member} has joined')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left')

@bot.event
async def on_ready():
    print('bot initialized')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('this is only a test'))

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


#Cog stuff

@bot.command()
async def load(ctx, extension): #extension is cog
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("loaded cog")

@bot.command()
async def unload(ctx, extension): #extension is cog
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("unloaded cog")

@bot.command()
async def reload(ctx, extension): #extension is cog
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("reloaded cog")

#search cog folder for .py files
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')


#####################DISCORD GAME###########################################

@bot.command()
async def ping(ctx):
    await ctx.send(f'ur ping is {bot.latency*1000} ms')
@bot.command()
async def beginGame(ctx):
    msg = await ctx.send('press the check below if you would like to join the game')
    await msg.add_reaction("\u2705")
    ctx.author.send(f'{user.name} has been added to the game')

@bot.event
async def on_reaction_add(reaction, user):
#    userCount+=1
    channel=reaction.message.channel
#    id=payload.message_id
    id=user.id
    user=bot.get_user(id)
    if reaction.emoji=='\u2705':  
        await user.send('you have joined the game')
        print('a player has joined')
    await channel.send(f'{user.name} has added {reaction.emoji} in {channel}')
    return True
@bot.event
async def on_reaction_remove(reaction, user):
    channel=reaction.message.channel
    await channel.send(f'{user.namedfa} has removed {reaction.emoji} in {channel}')
    
@bot.command()
async def dm(ctx, message):
    await ctx.author.send(message)
    
#dereks learning function    
@bot.command()
async def printCards(ctx):
    cards = ["blue", "black", "red"]
    for x in cards:
        await ctx.send(x)

bot.run('NzU5MTc0MzUxMzQxMjIzOTU2.X25qNg.-_PsN-qFJaiqt0VaPPg6brDhA2s')