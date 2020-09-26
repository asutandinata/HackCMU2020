import discord
from discord.ext import commands
import os

class GameCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("game cod enables")

    @commands.command()
    async def pepegga(self,ctx):
        await ctx.send("peepo pog")

    async def on_message(self, message):
        print(message.content)

def setup(bot):
    bot.add_cog(GameCog(bot))