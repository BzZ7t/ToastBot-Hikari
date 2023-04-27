#-------------> Imports
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
@lightbulb.command('roll',
                   'Roll a dice')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def roll(ctx):
    high_no = int(ctx.options.number)
    await ctx.respond(f"You rolled a **{random.randint(1, high_no)}**!")
    
    #TODO: int/str checker
    '''if high_no == int:
        await ctx.respond("That is not a number, please try again")
        time.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again.")
        time.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again..")
        time.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again...")
        time.sleep(1)
        await ctx.delete_last_response()###
        
    else:
        await ctx.respond(f"You rolled a **{random.randint(1, high_no)}**!")'''
        
    

def load(bot):
    bot.add_plugin(plugin)
