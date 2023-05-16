import asyncio
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("interact")

#---> Common Varibles 
dgg = False
#---> Common Functions

#---------------------------> function for simple user interactions based on list file and gif list files 
async def simple_interaction(ctx, interaction):
    user_ran = f"<@{ctx.author.id}>"
    user_interact = ctx.options.user
    #TODO: File open when fstring found: open("./plugins/assets/interact/hug_list.txt", "r").read().split("\n")
    list = open(f"./plugins/assets/interact/{interaction}_list.txt", "r").read().split("\n")
    list_gif = open(f"./plugins/assets/interact/{interaction}_list_gif.txt", "r").read().split("\n")
    
    if ctx.options.gif == True:
        await ctx.respond(f"{list[random.randint(0,len(list))]}\n{list_gif[random.randint(0,len(list_gif))]}".format(user_ran = user_ran, user_interact = user_interact),
                          user_mentions=True)
    else:
        await ctx.respond({list[random.randint(0,len(list))]})


# ----> '/interact' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def interact():
    pass

#---------------------------------> /interact hug 
@interact.child
@lightbulb.option('gif',
                  "add a gif to the message?", required=False, default=False,
                  choices=[hikari.CommandChoice(name='Yes', value=True),
                           hikari.CommandChoice(name='No', value=False)],
                  type=bool)
@lightbulb.option('user',
                  'Who would you like to hug?', required=True)
@lightbulb.command('hug',
                   'give another user a hug!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hug(ctx):
    await simple_interaction(ctx, interaction='hug')
        
@interact.child
@lightbulb.option('gif',
                  "add a gif to the message? ('Yes/No' or 'y/n')", required=False, default=False,
                  choices=[hikari.CommandChoice(name='Yes', value=True),
                           hikari.CommandChoice(name='No', value=False)],
                  type=bool)
@lightbulb.option('user',
                  'Who would you like to boop?')
@lightbulb.command('boop',
                   'boop another user.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def boop(ctx):
    simple_interaction(ctx, interaction='boop')
        
#-----------> More complex interactions,
#---------------------------------> /interact violence user:

def load(bot):
    bot.add_plugin(plugin)
