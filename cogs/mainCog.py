import discord
from discord.ext import commands
from eventManager import EventManager
import os

class MainCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("gray squirrelssssss")

    @commands.command()
    async def ping2(self,ctx):
        await ctx.send("POG")

def setup(bot):
    bot.add_cog(MainCog(bot))