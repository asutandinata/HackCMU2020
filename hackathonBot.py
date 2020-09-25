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
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('this is only a test'))
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

#search cog folder for .py files
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run('NzU5MTc0MzUxMzQxMjIzOTU2.X25qNg.-_PsN-qFJaiqt0VaPPg6brDhA2s')