import discord
from discord.ext import commands
import os


class Player(commands.Cog):
    
    id=0
    balance = 0
    rent = {}
    properties = {}
    actionCard = {}


    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("Player Cog enabled")

    @commands.command()
    async def withdraw(self, ctx, withdrawAmount):
        if(self.balance - withdrawAmount < 0):
            await ctx.send("Not enough money!")
        else:
            self.balance -= withdrawAmount

    @commands.command()
    async def deposit(self, depositAmount):
        self.balance += depositAmount

    @commands.command()
    async def getBalance(self,ctx):
        await ctx.send(self.balance)

    @commands.command()
    async def getproperties(self,ctx):
        await ctx.send(self.properties)

    @commands.command()
    async def getRent(self,ctx):
        await ctx.send(self.rent)

def setup(bot):
    bot.add_cog(Player(bot))