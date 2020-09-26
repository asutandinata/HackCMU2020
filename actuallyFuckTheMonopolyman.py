import discord
from discord.ext import commands
import os



###########HACKATHON MAIN################
id1=0
id2=0

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

'''
#search cog folder for .py files
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')
'''

#####################DISCORD GAME###########################################

@bot.command()
async def ping(ctx):
    await ctx.send(f'ur ping is {bot.latency*1000} ms')
@bot.command()
async def beginGame(ctx):
    msg = await ctx.send('press the green or blue check below if you would like to join the game')
    await msg.add_reaction("\u2705")
    await msg.add_reaction("\u2611")
    ctx.author.send(f'{user.name} has been added to the game')

@bot.event
async def on_reaction_add(reaction, user):
    channel=reaction.message.channel
    if reaction.emoji=='\u2705':  
        id1=user.id
        user=bot.get_user(id1)
        await user.send('you have joined the game player 1')
        print('a player has joined')
        player1=player()
        player1.id=id1
        #create player 1 object here
    elif reaction.emoji=='\u2611':
        id2=user.id
        user=bot.get_user(id2)
        await user.send('you have joined the game player 2')
        print('a player has joined')
        player2=player()
        player2.id=id2
        #create player 2 object here

    
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

###########EVENT MANAGER#############

@commands.Cog.listener()
async def on_ready(): # self must be first parameter in every function in class
    print("event manager cog enables")

@commands.command()
async def isWinner(ctx, Player):
    await ctx.send(f'{Player} has won!')

@commands.command()
async def graySquirrelers(ctx):
    await ctx.send("SQUIRREL SQUIRREL SQUIRREL SQUIRREL")

@commands.command()
async def on_message(message):
    print(message.content)

@commands.command()
async def setPlayers(*args):
    for player in args:
        players += player
@commands.command()
async def playTurn():
    x = 42

@commands.command()
async def makeTurn(ctx, Player):
    x = 42

@commands.command()
async def transferMoney( ctx, Player1, Player2):
    x = 42
@commands.command()

async def dispTable(ctx, id, player1, player2):

    tableProp = player1.properties + player2.properties
    user=bot.get_user(id)
    for i in len(tableProp):
        imageVal = tableProp[i]
        await user.send(file=discord.File(f'{imageVal}.png'))

# card functions
# play hand
# display table
@commands.command()
async def trasferMoney(ctx, player1, player2, amount):
    # self.withde
        player1.withdraw(player1, ctx, amount)
        player2.deposit(player2,ctx,amount)
        #self.withdraw(Player1,ctx,amount)        
#############PLAYER#################


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
#######################

def setup(bot):
    bot.add_cog(EventManager(bot))
    bot.add_cog(Player(bot))
   

bot.run('NzU5MTc0MzUxMzQxMjIzOTU2.X25qNg.-_PsN-qFJaiqt0VaPPg6brDhA2s')
