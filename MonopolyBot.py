import discord
from discord.ext import commands
import os
import random
import math

#############PLAYER#################


class Player(commands.Cog):
    
    id=0
    balance = 100
    rent = []
    properties = []
    actionCard = []
    won=False
    houses = 0
    isTurn=False
    played = 0
    canDraw=True
    hand=[]
    fullSets = 0

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # self must be first parameter in every function in class
        print("Player Cog enabled")

    # def addProperties(self, id):
    #     self.properties.append(id)
    
    # def addActionCard(self, id):
    #     self.actionCard.append(id)

    # def addRent(self, id):
    #     self.rent.append(id)

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
deck = list(range(37))
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
        player1.isTurn=True
        player1.properties=[1,2]
        player1.rent=[11]
        player1.actionCard=[16, 34]
        print('drawing player 1 cards')
        # drawCard(player1)
        # drawCard(player1)
        # drawCard(player1)
        # drawCard(player1)
        # drawCard(player1)
        # player1.actionCard=[16, 21, 25]
        # player1.rent=[11]
        # player1.properties=[2]
    if reaction.emoji=='\u2611':
        id2=user.id
        user=bot.get_user(id2)
        await user.send('you have joined the game player 2')
        player2.id=id2
        player2.isTurn=False
        print('drawing player 2 cards')
        player2.properties = []
        player2.rent = []
        player2.actionCard=[]
        drawCard(player2)
        drawCard(player2)
        drawCard(player2)
        drawCard(player2)
        drawCard(player2)
        # player2.actionCard=[17, 23]
        # player2.rent=[12, 14]
        # player2.properties=[5]

    print(player1.properties)
    print(player2.properties)
    
     
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
    elif(ctx.author.id==player2.id):
        player= player2
    if(not player.isTurn): 
        await ctx.author.send("it's not your turn. Please wait until the other player has finished")
    elif(not player.canDraw):
        await ctx.author.send('you have drawn the maximum number of cards for this turn already')
    elif(player.isTurn and player.canDraw):
        prevBalance=player.balance
        drawCard(player)
        await ctx.author.send("you've just drawn a card! this is your deck now:")
        if(prevBalance<player.balance):
            await ctx.author.send(f'you have gained {player.balance-prevBalance} dollars')
        player.canDraw=False
        player.hand=player.properties+player.rent+player.actionCard
        for i in range(len(player.hand)):
            imageVal=player.hand[i]
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
async def endTurn(ctx):
    p1=bot.get_user(player1.id)
    p2=bot.get_user(player2.id)
    if(ctx.author.id==player1.id):
        player1.isTurn=False
        player2.isTurn=True
        await p1.send('you have finished your turn')
        await p2.send('it is your turn now')
    elif(ctx.author.id==player2.id):
        player2.isTurn=False
        player1.isTurn=True
        await p2.send('you have finished your turn')
        await p1.send('it is your turn now')
    player1.played = 0
    player2.played = 0
    player1.canDraw=True
    player2.canDraw=True
    print(player1.isTurn, player2.isTurn)
@bot.command()
async def play(ctx, id):
    id=int(id)
    
    if(ctx.author.id==player1.id):
        player=player1
        opponent=player2
    elif(ctx.author.id==player2.id):
        player=player2
        opponent=player1
    if(player.isTurn and player.played<2):
        if(id<11):
            await ctx.author.send('not a valid play, you can only play rent or action cards')
        if(11<=id and id<=15):#charge other player rent
            if(len(player.rent)>0):
                if(checkFullSets(ctx, player)):
                    transferMoney(player,opponent, 200+(100 * player.houses))
                    await ctx.author.send('successfully played a rent card')
                    removeRentCard(id, player)
                    player.played+=1
                else:
                    await ctx.author.send("you don't have a full set")
            else:
                await ctx.author.send("you don't have a rent card")
        elif(16<=id and id<=20):#house card
            if(containsHouse(player)):
                if(checkFullSets(ctx, player)):
                    player.houses+=1
                    removeActionCard(id, player)
                    await ctx.author.send('successfully played a house card')
                    player.played+=1

                else:
                    await ctx.author.send("you don't have a full set")
            else:await ctx.author.send("you don't have a house card")
                
        elif(id==21 or id==22):#it's my birthday card
            if(containsBirthday(player)):
                transferMoney(player ,opponent, 200)
                player.played+=1
                await ctx.author.send("you have successfully played your birthday card")
                removeActionCard(id, player)
                #remove birthdaycard
            else:await ctx.author.send("you don't have a birthday card")

        if(id==23 or id==24):#double rent play
            if(containsDoubleRent(player)):
                if(checkFullSet(ctx, player) and check(len(player.rent)>0)):
                    player.played+=1
                    print("checkFullSet is true")
                    transferMoney(ctx,player,opponent, 400)
                    removeRentCard(id, player)
                    #  remove double rent card
                else: ctx.author.send('you either dont have a full set, or are missing rent cards')
            else:await ctx.author.send("you don't have a double rent card")
            
        if(id==25 or id==26):#pass go, draw 2 cards
            if(containsPassGo(player)):
                for i in range(2):
                    drawCard(player)
                await ctx.author.send("you have succesfully played your pass go card")
                player.played+=1
                removeActionCard(id, player)
            else:await ctx.author.send("you don't have a pass go card")
        if(id==27):
            if(containsDebtCollector(player)):
                await ctx.author.send("you have successfully played your debt collector card")
                transferMoney(ctx,player,opponent, 500)
                removeActionCard(id, player)
                player.played+=1
            else: await ctx.author.send('you do not have a debt collector card')
        checkWin(ctx, player)
    elif(opponent.isTurn):await ctx.author.send("it's not your turn. Please wait until the other player has finished")
    elif(player.played>=2):await ctx.author.send("you have played the max number of cards in your turn, please end your turn with /endTurn")
    

@bot.command()
async def bal(ctx):
    if(ctx.author.id==player1.id):
        await ctx.author.send(player1.balance)
    elif(ctx.author.id==player2.id):
        await ctx.author.send(player2.balance)

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

def checkWin(ctx, player):
    if(player == player1):
        if(player1.checkFullSet(ctx, player) >= 2):
            isWinner(ctx, player)
            return True
        elif(player2.getBalance() < 0):
            isWinner(ctx, player)
            return True    
    elif(player == player2):
        if(player1.checkFullSet(ctx, player) >= 2):
            isWinner(ctx, player)
            return True
        elif(player2.getBalance() < 0):
            isWinner(ctx, player)
            return True    
    else:
        return False
def containsHouse(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==16 or player.actionCard[i]==17 or player.actionCard[i]==18 or player.actionCard[i]==19 or player.actionCard[i]==20):
            counted+=1
    if(counted>0):return True
    else:return False
def containsDebtCollector(player):
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==27):
            counted+=1
    if(counted>0):return True
    else:return False       
def containsRent(player):
    if(len(player.rent)>0):return True
    else:return False

def containsBirthday(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==21 or player.actionCard[i]==22):
            counted+=1
    if(counted>0):return True
    else:return False
    
def containsDoubleRent(player):
    if(23 in player.actionCard or 24 in player.actionCard):return True
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
    

def checkFullSets(ctx, player):
    sortArrays()
    fullSets = 0
    red = 0
    for i in range(0, len(player.properties)):
        if((player.properties[i] == 0 and player.properties[i+1] == 1) or 
        (player.properties[i] == 0 and player.properties[i+1] == 2) or (player.properties[i] == 1 and player.properties[i+1] == 2)):
            red = 1
        if(player.properties[i] == 3 and player.properties[i+1] == 4):
            fullSets += 1
        if(player.properties[i] == 5 and player.properties[i+1] == 6):
            fullSets += 1
        if(player.properties[i] == 7 and player.properties[i+1] == 8):
            fullSets += 1
        if(player.properties[i] == 9 and player.properties[i+1] == 10):
            fullSets += 1
    return fullSets + red

def transferMoney(player, opponent, amount):
    player.balance+=amount
    opponent.balance-=amount
    if(opponent.balance<0):
        player.won=True

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

def drawCard(player):
    i = random.randint(0, len(deck)-1)
    if( 0 <= deck[i] and deck[i] <= 10):
        #player.addProperties(deck[i])
        a=deck[i]
        player.properties.append(a)
        deck.pop(i)   
    elif(10 < deck[i] and deck[i] <= 15):
        #player.addRent(deck[i])
        a=deck[i]
        player.rent.append(a)
        deck.pop(i)   
    elif(15 < deck[i] and deck[i] <= 27):
        #player.addActionCard(deck[i])
        a=deck[i]
        player.actionCard.append(a)
        deck.pop(i)   
    elif(27 < deck[i] and deck[i] < 37):
        a=deck[i]
        player.deposit(math.ceil((a-27)/2)*100)
        print("gained money")     
        deck.pop(i)          

def removeActionCard(id, player):   
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
