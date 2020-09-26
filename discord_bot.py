import discord
from discord.ext import commands

import random
import os
import string

#from /cogs/mainCog import *

bot=commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('gray squirrel')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined')
@bot.event
async def on_member_remove(member):
    print(f'{member} has left')
@bot.command()
async def pinger(ctx):
    await ctx.send(f'ur gey boi ping is {bot.latency*1000} ms')
@bot.command()
async def graySquirrel(ctx):
    await ctx.send("swish your bushy tail")




@bot.command()
async def load(ctx, extension): #extension is cog
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension): #extension is cog
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')




'''
@bot.command()
async def callMainCog(ctx):
    MainCog.acommand(ctx)

'''

@bot.command()
async def repeat(ctx, *args):
    fullString = ""
    for word in args:
        fullString += (" " + word)
    await ctx.send(fullString)



class squirrel(commands.Cog):
    squirrelColor = "gray"

    @commands.command()
    async def squirrelColorDeclare(self,ctx,args):
        squirrelColor = args
        await ctx.send(squirrelColor)

'''

class Economy(commands.Cog):

    async def withdraw_money(self, member, money):
        member.balance -= money
        

    async def deposit_money(self, member, money):
        member.balance == money


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def coinflip(self):
        return random.randint(0, 1)

    @commands.command()
    async def gamble(self, ctx, money: int):
        """Gambles some money."""
        economy = self.bot.get_cog('Economy')
        if economy is not None:
            await economy.withdraw_money(ctx.author, money)
            if self.coinflip() == 1:
                await economy.deposit_money(ctx.author, money * 1.5)
'''

#run actual bot
#bot.load_extension("cogs.MainCog")
#bot.add_cog(mainCog(bot))

bot.run('NzU5MTY0MjYxNzI0ODQ4MTQ4.X25g0A.9drjnmy12qRPmU5GlPB0EiwpcUQ')
