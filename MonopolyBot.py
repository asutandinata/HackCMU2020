import discord
from discord.ext import commands
import os
import random

#############PLAYER#################


class Player(commands.Cog):
    
    id=0
    balance = 100
    rent = []
    properties = []
    actionCard = []
    won=False


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
    msg = await ctx.send('react with the green check to be player 1, or react with the blue check to be player 2')
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
        player1.actionCard=[16, 21, 25]
        player1.rent=[11]
        player1.properties=[2]
    elif reaction.emoji=='\u2611':
        id2=user.id
        user=bot.get_user(id2)
        await user.send('you have joined the game player 2')
        player2.id=id2
        player2.actionCard=[17, 23]
        player2.rent=[12, 14]
        player2.properties=[5]

def beginningCardsP1():
    for i in range(5):
        drawCard(player1)

def beginningCardsP2():
    for i in range(5):
        drawCard(player2)  
     
@bot.command()
async def identify(ctx):
    if(ctx.author.id==player1.id):
         await ctx.author.send('you are player 1')
    elif(ctx.author.id==player2.id):
         await ctx.author.send('you are player 2')
@bot.command()
async def draw(ctx):
    if(ctx.author.id==player1.id):
        player= player1
        drawCard(player1)
    elif(ctx.author.id==player2.id):
        player= player2
        drawCard(player2)
    await ctx.author.send("you've just drawn a card! this is your deck now:")
    if(ctx.author.id==player1.id):
        hand=player1.properties+player1.rent+player1.actionCard
    elif(ctx.author.id==player2.id):
        hand=player2.properties+player2.rent+player2.actionCard
    for i in range(len(hand)):
        imageVal=hand[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))
    await ctx.author.send('end of your cards') 

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
async def printTable(ctx):
    await ctx.author.send("player 1's properties")  
    for i in range(len(player1.properties)):
        imageVal = player1.properties[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))
    await ctx.author.send("player 2's properties") 
    for i in range(len(player2.properties)):
        imageVal = player2.properties[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))

@bot.command()
async def play(ctx, id):
    id=int(id)
    if(ctx.author.id==player1.id):
        player=player1
        opponent=player2
    elif(ctx.author.id==player2.id):
        player=player2
        opponent=player1
    if(id<11):
        await ctx.author.send('not a valid play, you can only play rent or action cards')
    if(11<=id and id<=15):#charge other player rent
        if(len(player.rent)>0):
            if(checkFullSet(ctx, player)):
                transferMoney(player,opponent, 200)
                #remove rent card
            else:
                await ctx.author.send("you don't have a full set")
        else:
            await ctx.author.send("you don't have a rent card")
    elif(16<=id and id<=20):#house card
        if(containsRent(player)):
            if(checkFullSet(ctx, player)):
                player1.properties+=1
                #remove house card
            else:
                await ctx.author.send("you don't have a full set")
        else:await ctx.author.send("you don't have a house card")
            
    elif(id==21 or id==22):#it's my birthday card
        if(containsBirthday(player)):
            transferMoney(ctx, player ,otherPlayerpponent, 200)
            await ctx.author.send("you have successfully played your birthday card")
            #remove birthday card
        else:await ctx.author.send("you don't have a birthday card")

    if(id==23 or id==24):#double rent play
        if(containsDoubleRent):
            if(checkFullSet(ctx, player)and check(len.player.rent>0)):
                transferMoney(ctx,player,opponent, 400)
            #remove rent card, remove double rent card
        else:await ctx.author.send("you don't have a double rent card")
        
    if(id==25 or id==26):#pass go, draw 2 cards
        if(containsPassGo):
            for i in range(2):
                drawCard(player)
            await ctx.author.send("you have succesfully played your pass go card")
            #remove pa
        else:await ctx.author.send("you don't have a pass go card")
    
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

def containsRent(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==16 or player.actionCard[i]==17 or player.actionCard[i]==18 or player.actionCard[i]==19 or player.actionCard[i]==20):
            counted+=1
    if(counted>0):return True
    else:return False

def containsBirthday(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==21 or player.actionCard[i]==22):
            counted+=1
    if(counted>0):return True
    else:return False
    
def containsDoubleRent(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==23 or player.actionCard[i]==24):
            counted+=1
    if(counted>0):return True
    else:return False

def containsPassGo(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==25 or player.actionCard[i]==26):
            counted+=1
    if(counted>0):return True
    else:return False
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
        if((player.properties[i] == 0 and player.properties[i+1] == 1) or 
        (player.properties[i] == 0 and player.properties[i+1] == 2) or (player.properties[i] == 1 and player.properties[i+1] == 2)):
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
def transferMoney(player, opponent, amount):
    player.balance+=amount
    opponent.balance-=amount
    if(opponent.balance<0):player.won=True
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

def drawCard(Player):
    i = random.randint(0, len(deck)-1)
    if(player1 == Player):
        player = player1
    else:
        player = player2
    print(i)
    print(deck[i])
    if(0 <= i and i < len(deck)):
        print("valid index")
    if(  0 <= deck[i] and deck[i] <= 10):
        player.properties.append(deck[i])
    elif(10 < deck[i] and deck[i] <= 15):
        player.rent.append(deck[i])
    elif(15 < deck[i] and deck[i] <= 26):
        player.actionCard.append(deck[i])
    deck.pop(i);          

def removeActionCard(id, player):
    #player.properties.remove(id)    
    player.actionCard.remove(id)
    deck.append(id)

def removeRentCard(id, player):
    player.rent.remove(id)
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
