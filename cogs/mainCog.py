import discord
from discord.ext import commands
import os


class MainCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #@commands.command(pass_context=True)

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("gray squirrelssssss")

    @commands.command()
    async def ping2(self,ctx):
        await ctx.send("POG")

    async def on_message(self, message):
        print(message.content)

def setup(bot):
    bot.add_cog(MainCog(bot))