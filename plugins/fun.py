#-------------> Imports
import asyncio
import random
import time

import hikari
import lightbulb

plugin = lightbulb.Plugin("fun")

#----> '/fun' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("fun",
                   "Do all the **fun** stuff :D")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def fun(ctx):
    pass
    
#----------------------------> /fun toast-insults
#----> responds with a random index from the list ""
@fun.child
@lightbulb.command('toast-insults',
                   'Make ToastBot reply with a toast-related insult')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toastinsult(ctx):
    insult = open("./plugins/assets/fun/toast-insults.txt", "r").read().split("\n")
    await ctx.respond(insult[random.randint(0,len(insult))])
    
@fun.child 
@lightbulb.option('number',
                  'whats the highest number the dice could roll?')
@lightbulb.command('diceroll',
                   'Roll a dice')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def roll(ctx):
    high_no = ctx.options.number
    
    try:
        high_no = int(high_no)
        await ctx.respond("You rolled a")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("You rolled a.")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("You rolled a..")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("You rolled a...")
        await asyncio.sleep(1)
        await ctx.edit_last_response(f"You rolled a **{random.randint(1, high_no)}**!")
    except:
        await ctx.respond("That is not a number, please try again")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again.")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again..")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again...")
        await asyncio.sleep(1)
        await ctx.delete_last_response()
        
@fun.child
@lightbulb.command('coinflip',
                   'flip a 50/50 coin!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def coinflip(ctx):
    coin_result = 'Tails'
    
    if random.randint(0,1) == 1:
        coin_result = 'Heads'
    
    await ctx.respond('The coin landed on')
    await asyncio.sleep(0.5)
    await ctx.edit_last_response('The coin landed on.')
    await asyncio.sleep(0.5)
    await ctx.edit_last_response('The coin landed on..')
    await asyncio.sleep(0.5)
    await ctx.edit_last_response('The coin landed on...')
    await asyncio.sleep(1)
    await ctx.edit_last_response(f'The coin landed on {coin_result}!')



def load(bot):
    bot.add_plugin(plugin)
