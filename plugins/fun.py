#-------------> Imports
import random

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

def load(bot):
    bot.add_plugin(plugin)
