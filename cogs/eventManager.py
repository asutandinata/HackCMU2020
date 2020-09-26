import discord
from discord.ext import commands
import os

class EventManager(commands.Cog):

    players = {}


    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("event manager cog enables")

    @commands.command()
    async def graySquirrelers(self,ctx):
        await ctx.send("SQUIRREL SQUIRREL SQUIRREL SQUIRREL")

    async def on_message(self, message):
        print(message.content)
    
    async def setPlayers(self, *args):
        for player in args:
            players += player
    
    async def playTurn(self):
        pass
        
def setup(bot):
    bot.add_cog(EventManager(bot))