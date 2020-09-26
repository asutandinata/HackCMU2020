import discord
from discord.ext import commands
import os
from cogs import player

class EventManager(commands.Cog):

    players = {}


    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("event manager cog enables")
    

    @commands.command()
    async def isWinner(self, ctx, Player):
        await ctx.send(f'{Player} has won!')

    @commands.command()
    async def graySquirrelers(self,ctx):
        await ctx.send("SQUIRREL SQUIRREL SQUIRREL SQUIRREL")

    @commands.command()
    async def on_message(self, message):
        print(message.content)
    
    @commands.command()
    async def setPlayers(self, *args):
        for player in args:
            players += player
    @commands.command()
    async def playTurn(self):
        x = 42

    @commands.command()
    async def makeTurn(self, ctx, Player):
        x = 42

    @commands.command()
    async def transferMoney(self, ctx, Player1, Player2):
        x = 42

    # card functions
    # play hand
    # display table


    @commands.command()
    async def trasferMoney(self, ctx, Player1, Player2, amount):
       # self.withde
        

        Player1.withdraw(Player1, ctx, amount)
        Player2.deposit(Player2,ctx,amount)


        EventManager.players

        #self.withdraw(Player1,ctx,amount)

        




        
def setup(bot):
    bot.add_cog(EventManager(bot))