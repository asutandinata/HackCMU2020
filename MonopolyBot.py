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
    latestCard=0

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
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('I love capitalism'))

@bot.command(brief='clears a certain amount of messages')
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

@bot.command(brief='calculates your ping')
async def ping(ctx):
    await ctx.send(f'ur ping is {bot.latency*1000} ms')
@bot.command(brief='starts up a game of monopoly deal')
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
        player1.properties=[]
        player1.rent=[]
        player1.actionCard=[]
        #print('drawing player 1 cards')
        for i in range(5):
            drawCard(player1)
    if reaction.emoji=='\u2611':
        id2=user.id
        user=bot.get_user(id2)
        await user.send('you have joined the game player 2')
        player2.id=id2
        player2.isTurn=False
        #print('drawing player 2 cards')
        player2.properties = []
        player2.rent = []
        player2.actionCard=[]
        for i in range(5):
            drawCard(player2)
        
  
    
     
@bot.command(brief='identifies what player number you are if you forget')
async def identify(ctx):
    if(ctx.author.id==player1.id):
         await ctx.author.send('you are player 1')
    elif(ctx.author.id==player2.id):
         await ctx.author.send('you are player 2')

@bot.command(brief='draws a card')
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
        await ctx.author.send("you've just drawn a card! this is what you just drew")
        if(prevBalance<player.balance):
            await ctx.author.send(f'you have gained {player.balance-prevBalance} dollars')
        player.canDraw=False
        player.hand=player.properties+player.rent+player.actionCard
        await ctx.author.send(file=discord.File(f'{player.latestCard}.png'))
        await ctx.author.send('end of your cards') 

    

@bot.command(brief='prints all cards in your deck')
async def printCards(ctx):
    if(ctx.author.id==player1.id):
        hand=player1.properties+player1.rent+player1.actionCard
    elif(ctx.author.id==player2.id):
        hand=player2.properties+player2.rent+player2.actionCard
    for i in range(len(hand)):
        imageVal=hand[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))  
    await ctx.author.send('end of your cards')  


@bot.command(brief='prints all properties each player has')    
async def printTable(ctx):
    await ctx.author.send("player 1's properties")  
    for i in range(len(player1.properties)):
        imageVal = player1.properties[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))
    await ctx.author.send("player 2's properties") 
    for i in range(len(player2.properties)):
        imageVal = player2.properties[i]
        await ctx.author.send(file=discord.File(f'{imageVal}.png'))
        
@bot.command(brief="ends a user's turn")
async def endTurn(ctx):
    p1=bot.get_user(player1.id)
    p2=bot.get_user(player2.id)
    if(ctx.author.id==player1.id):
        player1.isTurn=False
        player2.isTurn=True
        await p1.send('you have finished your turn')
        await p2.send('it is your turn now')
        await p2.send(f'you start off with a balance of ${player2.balance}')
    elif(ctx.author.id==player2.id):
        player2.isTurn=False
        player1.isTurn=True
        await p2.send('you have finished your turn')
        await p1.send('it is your turn now')
        await p1.send(f'you start off with a balance of ${player1.balance}')
    player1.played = 0
    player2.played = 0
    player1.canDraw=True
    player2.canDraw=True
    #print(player1.isTurn, player2.isTurn)
@bot.command(brief='play an action or rent card, done by typing /play CardID')
async def play(ctx, id):
    id=int(id)
    
    if(ctx.author.id==player1.id):
        player=player1
        opponent=player2
        opp=bot.get_user(player2.id)
    elif(ctx.author.id==player2.id):
        player=player2
        opponent=player1
        opp=bot.get_user(player1.id)
    if(player.isTurn and player.played<2):
        if(id<11):
            await ctx.author.send('not a valid play, you can only play rent or action cards')
        if(11<=id and id<=15):#charge other player rent
            if(len(player.rent)>0):
                if(checkFullSets(ctx, player)>0):
                    transferMoney(player,opponent, 200+(100 * player.houses))
                    await ctx.author.send('successfully played a rent card')
                    await opp.send(f'opponent played a rent card, you lost {200+(100 * player.houses)} dollars')
                    removeRentCard(id, player)
                    player.played+=1
                else:
                    await ctx.author.send("you don't have a full set")
            else:
                await ctx.author.send("you don't have a rent card")
        elif(16<=id and id<=20):#house card
            if(containsHouse(player)):
                if(checkFullSets(ctx, player)>0):
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
                await opp.send('opponent played a birthday card, you lost 200 dollars')
                removeActionCard(id, player)
                
                #remove birthdaycard
            else:await ctx.author.send("you don't have a birthday card")

        if(id==23 or id==24):#double rent play
            if(containsDoubleRent(player)):
                if(checkFullSets(ctx, player)>0 and (len(player.rent)>0)):
                    player.played+=1
                    print("checkFullSets is true")
                    transferMoney(player,opponent, 2*(200+(100 * player.houses)))
                    removeActionCard(id, player)#removes double rent
                    index=0
                    for i in range(len(player.rent)):
                        if(player.rent[i]>0):
                            index=int(player.rent[i])
                    await ctx.author.send("you have successfully played a double rent card")
                    await opp.send(f'double rent card, you have lost {2*(200+(100 * player.houses))} dollars')
                    removeRentCard(index, player)
                else: ctx.author.send('you either dont have a full set, or are missing rent cards')
            else:await ctx.author.send("you don't have a double rent card")
            
        if(id==25 or id==26):#pass go, draw 2 cards
            if(containsPassGo(player)):
                await ctx.author.send("you have succesfully played your pass go card")
                await ctx.author.send("you have recieved these 2 cards")
                for i in range(2):
                    await ctx.author.send(file=discord.File(f'{player.latestCard}.png'))
                    drawCard(player)
                player.played+=1
                removeActionCard(id, player)
            else:await ctx.author.send("you don't have a pass go card")
        if(id==27):
            if(containsDebtCollector(player)):
                await ctx.author.send("you have successfully played your debt collector card")
                await opp.send('opponent played debt collector, you lost $500')
                transferMoney(player,opponent, 500)
                removeActionCard(id, player)
                player.played+=1
            else: await ctx.author.send('you do not have a debt collector card')
        if(player.balance>0 and opponent.balance<0):
            await ctx.author.send("you have won by winning capitalism")
            await opp.send('you have lost by going bankrupt')
        elif(checkFullSets(ctx, player)>=2):
            await ctx.author.send("you have won by collecting 2 fulls sets")
            await opp.send('you have lost, other player collected 2 full sets')
    elif(opponent.isTurn):await ctx.author.send("it's not your turn. Please wait until the other player has finished")
    elif(player.played>=2):await ctx.author.send("you have played the max number of cards in your turn, please end your turn with /endTurn")
    

@bot.command(brief='returns your balance')
async def bal(ctx):
    if(ctx.author.id==player1.id):
        await ctx.author.send(player1.balance)
    elif(ctx.author.id==player2.id):
        await ctx.author.send(player2.balance)

@bot.command(brief='ends the current game')
async def endGame(ctx):   
    #player 1 reset variables
    player1.id=0
    player1.balance = 100
    player1.rent = []
    player1.properties = []
    player1.actionCard = []
    player1.won=False
    player1.houses = 0
    player1.isTurn=False
    player1.played = 0
    player1.canDraw=True
    player1.hand=[]
    player1.fullSets = 0
    player1.latestCard=0
####player 2 reset variables
    player2.id=0
    player2.balance = 100
    player2.rent = []
    player2.properties = []
    player2.actionCard = []
    player2.won=False
    player2.houses = 0
    player2.isTurn=False
    player2.played = 0
    player2.canDraw=True
    player2.hand=[]
    player2.fullSets = 0
    player2.latestCard=0

    
###########EVENT MANAGER#############

@commands.Cog.listener()
async def on_ready(): # self must be first parameter in every function in class
    print("event manager cog enables")

@commands.command()
async def isWinner(ctx, Player):
    await ctx.send(f'{Player} has won!')

def containsHouse(player):
    counted=0
    for i in range(len(player.actionCard)):
        if(player.actionCard[i]==16 or player.actionCard[i]==17 or player.actionCard[i]==18 or player.actionCard[i]==19 or player.actionCard[i]==20):
            counted+=1
    if(counted>0):return True
    else:return False
def containsDebtCollector(player):
    counted=0
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
    return int(fullSets + red)

def transferMoney(player, opponent, amount):
    player.balance+=amount
    opponent.balance-=amount
    if(opponent.balance<0):
        player.won=True

@commands.command()
async def on_message(message):
    print(message.content)


def drawCard(player):
    i = random.randint(0, len(deck)-1)
    if( 0 <= deck[i] and deck[i] <= 10):
        #player.addProperties(deck[i])
        a=deck[i]
        player.properties.append(a)
        player.latestCard=a
        deck.pop(i)   
    elif(10 < deck[i] and deck[i] <= 15):
        #player.addRent(deck[i])
        a=deck[i]
        player.rent.append(a)
        player.latestCard=a
        deck.pop(i)   
    elif(15 < deck[i] and deck[i] <= 27):
        #player.addActionCard(deck[i])
        a=deck[i]
        player.actionCard.append(a)
        player.latestCard=a
        deck.pop(i)   
    elif(27 < deck[i] and deck[i] < 37):
        a=deck[i]
        player.deposit(math.ceil((a-27)/2)*100)
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

@bot.command(brief='rules of monopoly deal')
async def rules(ctx):
    await ctx.send("Note: This game is currently only for 2 players")
    await ctx.send("1. Each player can draw 1 card during their turn.")
    await ctx.send("2. Each player can play up to 2 card during their turn.") 
    await ctx.send("3. If a player gets 2 sets of properties then they win.") 
    await ctx.send("4. If a player has a balance greater than 0 and the other player has a balance less than 0 the first player wins.")
    await ctx.send("5. Each action card has a special ability")
    await ctx.send("5a. 'rent' cards charge other players $200, but you can only use it when you have a fulls et of 2")
    await ctx.send("5b. 'double the rent' charges players double the rent, but can only be played with a rent card")
    await ctx.send("5c. 'houses' increase the rent for a set of properties by $100")
    await ctx.send("5d. 'it's my birthday' means all players have to give the player who played the it's my birthday card $200")
    await ctx.send("5e. 'Pass go' cards allow players to draw another 2 cards, regardless of how many they've drawn before")
    await ctx.send("6. Players start off with a balance of $100")
    await ctx.send("7. A player can skip their turn.")  


@bot.command(brief='credits')
async def about(ctx):
    await ctx.send("This bot was created by Anderson Sutandinata, Andrew Chong, and Derek Duenas.")
    await ctx.send("It was created in 24 hours during the HackCMU hackathon at Carnegie Mellon University.")
    
 
def setup(bot):
    bot.add_cog(EventManager(bot))
    bot.add_cog(Player(bot))
   
#please dont steal this run code it'll make me very upset-Anderson
bot.run('NzU5MTc0MzUxMzQxMjIzOTU2.X25qNg.-_PsN-qFJaiqt0VaPPg6brDhA2s')
