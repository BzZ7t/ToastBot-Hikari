#-------------> Imports
import random

import hikari
import lightbulb

plugin = lightbulb.Plugin("fun")

#----> Setting up the /fun group, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("fun",
                   "Do all the **fun** stuff :D")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def fun(ctx):
    pass
    
#----------------------------> /fun toast-insults
#----> opens file "strangeinsults.txt" and, line by line, adds to a list then responds with a random index from the list
@fun.child
@lightbulb.command('toast-insults',
                   'Make ToastBot reply with a toast-related insult')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toastinsult(ctx):
    content_list = ["You're just burnt toast :|",
                    "Eww, You crusty >~<",
                    "There's waaay better Toast in the Toastor o-o",
                    "I'm **GOLD** toast, you're burnt toast B3",
                    "I'm toasted, I'm **GOATed**!\nAfter I'm done with you, you'll be burnt and roasted B3"]
    await ctx.respond(content_list[random.randint(0,len(content_list))])
    

    
def load(bot):
    bot.add_plugin(plugin)
    
