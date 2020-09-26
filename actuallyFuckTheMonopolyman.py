import discord
from discord.ext import commands
import os
import random

#############PLAYER#################


class Player(commands.Cog):
    
    id=0
    balance = 0
    rent = []
    properties = []
    actionCard = []


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
bot=commands.Bot(command_prefix='/')

player1=Player(bot)
player2=Player(bot)
###########HACKATHON MAIN################
deck = list(range(27))
deck.pop(0)
#print(deck)


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

@bot.event
async def on_reaction_add(reaction, user):
    channel=reaction.message.channel
    if reaction.emoji=='\u2705':  
        id1=user.id
        user=bot.get_user(id1)
        await user.send('you have joined the game player 1')
        player1.id=id1
        for i in range(5):
            drawCard(player1)
    elif reaction.emoji=='\u2611':
        id2=user.id
        user=bot.get_user(id2)
        await user.send('you have joined the game player 2')
        player2.id=id2
        for i in range(5):
            drawCard(player2)
        
@bot.command()
async def printCards1(ctx):
    hand=player1.properties+player1.rent+player1.actionCard
    for i in range(len(hand)):
        imageVal=hand[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))  
        await ctx.author.send('end of your cards')

@bot.command()
async def printCards2(ctx):
    hand=player2.properties+player2.rent+player2.actionCard
    for i in range(len(hand)):
        imageVal=hand[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))
        await ctx.author.send('end of your cards')  

@bot.command()
async def play(ctx, id):
    if(11<=id and id<=15):#charge other player rent
        #if(#player has fuill set):
            transferMoney(ctx,player1,player2, 200)
            
    elif(16<=id and id<=20):
        #if(#player has fuill set):
            player1.properties+=1
            
    elif(21<=id and id<=22):
        transferMoney(ctx, player1,player2, 200)
        
    if(23<=id and id<=24):
        #if(#player has fuill set):
            transferMoney(ctx,player1,player2, 200)
        
    if(25<=id and id<=26):
        drawCards
    
@bot.command()
async def dm(ctx, message):
    await ctx.author.send(message)

###########EVENT MANAGER#############

@commands.Cog.listener()
async def on_ready(): # self must be first parameter in every function in class
    print("event manager cog enables")

@commands.command()
async def isWinner(ctx, Player):
    await ctx.send(f'{Player} has won!')

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
async def dispTable(ctx, id, player1, player2):
    tableProp = player1.properties + player2.properties
    user=bot.get_user(id)
    for i in len(tableProp):
        imageVal = tableProp[i]
        await user.send(file=discord.File(f'{imageVal}.png'))


def drawCard(player):
    i = random.randint(1, len(deck))
    print(i)
    print(deck[i])
    if(deck[i] <= 10):
        player.properties.append(i)
    elif(deck[i] <= 15):
        player.rent.append(i)
    else:
        player.actionCard.append(i)
    deck.pop(i);   

async def removeCard(id, player):
    player.properties.remove(id)
    deck.append(id)

@commands.command()
async def isHandSizeValid(player):
    if(len(rent)+len(actionCard) <= 7):
        return True
    else:
        return False

@commands.command()
async def trasferMoney(ctx, player1, player2, amount):
    # self.withde
        player1.withdraw(player1, ctx, amount)
        player2.deposit(player2,ctx,amount)
        #self.withdraw(Player1,ctx,amount)        


def setup(bot):
    bot.add_cog(EventManager(bot))
    bot.add_cog(Player(bot))
   

bot.run('NzU5MTc0MzUxMzQxMjIzOTU2.X25qNg.-_PsN-qFJaiqt0VaPPg6brDhA2s')
