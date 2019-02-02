import discord
from discord.ext import commands
import asyncio
import time
import random
import subprocess
import math

f = open("keys.txt", "r")
key = f.readline().strip()
serverID= int(f.readline().strip())
TOKEN = key

bot = commands.Bot(command_prefix='!') #Sets up the command prefix
bombSignal="!!!"
emoteConverter={'0':':zero:', '1':':one:', '2':':two:', '3':':three:', '4':':four:', '5':':five:', '6':':six:', '7':':seven:', '8':':eight:', '!!!':':bomb:'}

@bot.event #logs in
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def boardBuilder(size):
    #size is sqrt of board size, for example, 8 is an 8 x 8 board
    bombNum = size+math.floor(math.sqrt(size))
    board=[[None]*size for x in range(size)]
    for i in range(bombNum): #Effectively a bomb placing function
        success=False
        while success==False:
            xcoord= random.randint(0,size-1)
            ycoord=random.randint(0,size-1)
            if board[xcoord][ycoord] == None:
                board[xcoord][ycoord]=bombSignal
                success=True
    for i in range(size): #Places the numbers on the board
        for j in range(size):
            count = 0
            if board[i][j] != bombSignal:
                for counteri in range(-1,2):
                    for counterj in range(-1,2):
                        try:
                            if board[i+ counteri][j+counterj]==bombSignal:
                                if i +counteri==-1 or j +counterj ==-1:
                                    count+=0
                                else:
                                    count+=1
                        except IndexError:
                            break
                board[i][j]=str(count)
    return board

def emotify(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            arr[i][j]=emoteConverter[arr[i][j]]
    return arr
                
def Spoilify(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            arr[i][j]="||"+arr[i][j]+"||"
    return arr

@bot.command()
async def sweep(ctx, size):
    if int(size) <=1:
        await ctx.send("Pwease don't bweak me senpai UwU")
    elif int(size) > 12:
        await ctx.send("Please pick a number between 2 and 12 to accomodate for mobile users")
    else:
        for arr in Spoilify(emotify(boardBuilder(int(size)))):
            line=" ".join(str(ele) for ele in arr)
            await ctx.send(line)

@bot.command()
async def deletemsgs(ctx, number):
    general = bot.get_channel(serverID)
    await general.purge(limit=int(number), check=None, before=None, after=None, around=None, reverse=False, bulk=True)


bot.run(TOKEN) #fires up the bot
