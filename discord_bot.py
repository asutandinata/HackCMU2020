import discord
from discord.ext import commands

bot=commands.Bot(command_prefix='.')
@bot.event
async def on_ready():
    print('began')
@bot.event
async def on_member_join(member):
    print(f'{member} has joined')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left')
@bot.command()
async def ping(ctx):
    await ctx.send(f'ur ping is {bot.latency*1000} ms')
@bot.command()
async def fuck(ctx):
    await ctx.send("no that's gay")
bot.run('NzU5MTY0MjYxNzI0ODQ4MTQ4.X25g0A.9drjnmy12qRPmU5GlPB0EiwpcUQ')
