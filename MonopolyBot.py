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

    
    async def withdraw(self, ctx, withdrawAmount):
        if(self.balance - withdrawAmount < 0):
            await ctx.send("Not enough money!")
        else:
            self.balance -= withdrawAmount

    
    def deposit(self, depositAmount):
        self.balance += depositAmount

    
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
#deck.pop(0)
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
async def printCards(ctx):
    if(ctx.author.id==player1.id):
        hand=player1.properties+player1.rent+player1.actionCard
    elif(ctx.author.id==player2.id):
        hand=player2.properties+player2.rent+player2.actionCard
    for i in range(len(hand)):
        imageVal=hand[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))  
    await ctx.author.send('end of your cards')        


@bot.command()
async def play(ctx, id):
    id=int(id)
    if(ctx.author.id==player1.id):
        player=player1
        opponent=player2
    elif(ctx.author.id==player2.id):
        player=player2
        opponent=player1
    if(11<=id and id<=15):#charge other player rent
        if(checkFullSet(player)):
            transferMoney(ctx,player,opponent, 200)
            #remove rent card
        else:
            await ctx.author.send("you don't have a full set")
    elif(16<=id and id<=20):
        if(checkFullSet(player)):
            player1.properties+=1
            
    elif(21<=id and id<=22):#it's my birthday card
        transferMoney(ctx, player ,otherPlayerpponent, 200)

    if(23<=id and id<=24):#double rent play
        if(checkFullSet(player)and check(len.player.rent>0)):
            transferMoney(ctx,player,opponent, 400)
            #remove rent card, remove double rent card
    if(25<=id and id<=26):#pass go, draw 2 cards
        for i in range(2):
            drawCard(player)
            await ctx.author.send("you have succesfully played your pass go card")
    
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

def sortArrays():    
    player1.properties.sort()
    player1.rent.sort()
    player1.actionCard.sort()
    player2.properties.sort()
    player2.rent.sort()
    player2.actionCard.sort()
    

def checkFullSet(ctx, player):
    sortArrays()
    for i in range(0,10):
        if(player.properties[i] == 1 and player.properties[i+1] == 2):
            return True
        if(player.properties[i] == 3 and player.properties[i+1] == 4):
            return True
        if(player.properties[i] == 5 and player.properties[i+1] == 6):
            return True
        if(player.properties[i] == 7 and player.properties[i+1] == 8):
            return True
        if(player.properties[i] == 9 and player.properties[i+1] == 10):
            return True
    return False

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
    i = random.randint(0, len(deck))
    print(i)
    print(deck[i])
    print(deck[0])
    if(0 <= i and i < len(deck)):
        print("valid index")
    if(deck[i] <= 10):
        player.properties.append(i)
    elif(deck[i] <= 15):
        player.rent.append(i)
    else:
        player.actionCard.append(i)
    deck.pop(i);   

def removeCard(id, player):
    player.properties.remove(id)
    deck.append(id)

@commands.command()
async def isHandSizeValid(player):
    if(len(rent)+len(actionCard) <= 7):
        return True
    else:
        return False


def trasferMoney(ctx, player1, player2, amount):
        player1.withdraw(player1, ctx, amount)
        player2.deposit(player2,ctx,amount)
        #self.withdraw(Player1,ctx,amount)        


def setup(bot):
    bot.add_cog(EventManager(bot))
    bot.add_cog(Player(bot))
   

bot.run('NzU5MTc0MzUxMzQxMjIzOTU2.X25qNg.-_PsN-qFJaiqt0VaPPg6brDhA2s')
