import discord
import asyncio
from discord.ext import commands

COMMAND_PREFIX = '$'

currentTipJar = []

GAME_IN_PROGRESS = False


#Tip Jar Visual Settings
TIP_JAR_DRAWING_HEADER = '\n--------------------------------------------------\n-                             TIP JAR                                  -'
TIP_JAR_DRAWING_SIDE = ' '
TIP_JAR_DRAWING_BOTTOM = '--------------------------------------------------'
TIP_JAR_DRAWING_EMPTY = '\n-                                                                             -'

# How much space to put in between the header and the characters, and the characters and the bottom
TIP_JAR_PADDING = 2;


with open('Token.txt', 'r') as token_file:
    token = token_file.readline()

intents = discord.Intents.all()

bot = commands.Bot(COMMAND_PREFIX, intents = intents)


@bot.command()
async def TipJarDrawing(ctx: commands.Context):
    global TIP_JAR_DRAWING
    await ctx.send(TIP_JAR_DRAWING)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('waiting...'))


# Start Game Command - Sets a new tip jar based on names
@bot.command(aliases=['start', 'sg', 'new', 'sugma'])
async def StartGame(ctx: commands.Context, *names):
    global currentTipJar, GAME_IN_PROGRESS, TIP_JAR_DRAWING_HEADER, TIP_JAR_DRAWING_BOTTOM, TIP_JAR_DRAWING_SIDE, TIP_JAR_PADDING, TIP_JAR_DRAWING_EMPTY
    if(GAME_IN_PROGRESS):
        await ctx.send("A game is already occuring!")
        return

    GAME_IN_PROGRESS = True
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Tip Jar'))


    currentTipJar = list(names)

    # Display Jar
    final = "Our candidates for the tip Jar are:"
    final = final + TIP_JAR_DRAWING_HEADER
    final = final + TIP_JAR_DRAWING_EMPTY * TIP_JAR_PADDING
    for i in range(len(currentTipJar)):
        final = final + ('{:<7} {:^60} {:>7}'.format('\n' + TIP_JAR_DRAWING_SIDE, ('**' + currentTipJar[i] + '**'), TIP_JAR_DRAWING_SIDE))
    final = final + TIP_JAR_DRAWING_EMPTY * TIP_JAR_PADDING
    final = final + ('\n' + TIP_JAR_DRAWING_BOTTOM)

    await ctx.send(final)

# Start Game Command Error Handler
@StartGame.error
async def startgame_error(ctx: commands.Context, error):
    await ctx.send(error)


# View Tip Jar command - displays the current names in the tip jar
@bot.command(aliases=['t', 'Tip', 'T', 'tip', 'throwers', 'view', 'View'])
async def TipJar(ctx: commands.Context):
    global currentTipJar, GAME_IN_PROGRESS, TIP_JAR_DRAWING_HEADER, TIP_JAR_DRAWING_BOTTOM, TIP_JAR_DRAWING_SIDE, TIP_JAR_PADDING, TIP_JAR_DRAWING_EMPTY
    if(not GAME_IN_PROGRESS):
        await ctx.send("A game is not currently occurring.")
        return

    if(len(currentTipJar) == 0):
        await ctx.send("Nobody is in the tip jar!")
        return

    final = "Here is our current tip jar:"
    final = final + TIP_JAR_DRAWING_HEADER
    final = final + TIP_JAR_DRAWING_EMPTY * TIP_JAR_PADDING
    for i in range(len(currentTipJar)):
        final = final + ('{:<7} {:^60} {:>7}'.format('\n' + TIP_JAR_DRAWING_SIDE, ('**' + currentTipJar[i] + '**'), TIP_JAR_DRAWING_SIDE))
    final = final + TIP_JAR_DRAWING_EMPTY * TIP_JAR_PADDING
    final = final + ('\n' + TIP_JAR_DRAWING_BOTTOM)

    await ctx.send(final)
    
# View Tip Jar Error Handler
@TipJar.error
async def tipjar_error(ctx: commands.Context,error):
    await ctx.send(error)

# Clear the Entire Jar
@bot.command(aliases=['c', 'clear', 'Clear', 'C'])
async def ClearJar(ctx: commands.Context):
    global currentTipJar, GAME_IN_PROGRESS

    if(not GAME_IN_PROGRESS):
        await ctx.send("A game is not currently occurring.")
        return

    currentTipJar = []
    await ctx.send("Tip jar has been cleared!")


# Add a singular name to the tip jar
@bot.command(aliases=['Add', 'add', 'losar'])
async def AddToJar(ctx: commands.Context, name):
    global currentTipJar, GAME_IN_PROGRESS
    if(not GAME_IN_PROGRESS):
        await ctx.send("A game is not currently occurring.")
        return

    currentTipJar.append(name)
    await ctx.send(name + " has been added to the tip jar!")

@AddToJar.error
async def addtojar_error(ctx: commands.Context, error):
    await ctx.send(error)


# Remove from jar function
@bot.command(aliases=['winar', 'remove', 'Remove'])
async def RemoveFromJar(ctx: commands.Context, name):
    global GAME_IN_PROGRESS
    if(not GAME_IN_PROGRESS):
        await ctx.send("A game is not currently occurring.")
        return

    if(name in currentTipJar):
        currentTipJar.remove(name)
        # await ctx.send(name + " has been removed from the tip jar!")
        await ctx.send(name + " did something!")
    else:
        await ctx.send(name + " is not in the tip jar!")

# Remove from jar error handler
@RemoveFromJar.error
async def removefromjar_error(ctx: commands.Context, error):
    await ctx.send(error)

# End the current game and display the final tip jar stats
@bot.command(aliases=['end', 'End'])
async def EndGame(ctx: commands.Context):
    global currentTipJar, GAME_IN_PROGRESS, TIP_JAR_DRAWING_HEADER, TIP_JAR_DRAWING_BOTTOM, TIP_JAR_DRAWING_SIDE, TIP_JAR_PADDING, TIP_JAR_DRAWING_EMPTY
    if(not GAME_IN_PROGRESS):
        await ctx.send("A game is not even going you bozo.")
        return
    
    GAME_IN_PROGRESS = False
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('waiting...'))

    if(len(currentTipJar) == 0):
        await ctx.send("Nobody was in the tip jar!")
        return

    final = "Here is our final tip jar:"
    final = final + TIP_JAR_DRAWING_HEADER
    final = final + TIP_JAR_DRAWING_EMPTY * TIP_JAR_PADDING
    for i in range(len(currentTipJar)):
        final = final + ('{:<7} {:^60} {:>7}'.format('\n' + TIP_JAR_DRAWING_SIDE, ('**' + currentTipJar[i] + '**'), TIP_JAR_DRAWING_SIDE))
    final = final + TIP_JAR_DRAWING_EMPTY * TIP_JAR_PADDING
    final = final + ('\n' + TIP_JAR_DRAWING_BOTTOM)

    await ctx.send(final)

    currentTipJar = []

@EndGame.error
async def endgame_error(ctx: commands.Context, error):
    await ctx.send(error)


bot.run(token)