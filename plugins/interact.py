import asyncio
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("interact")

#---> Common Varibles 

#---> Common Functions

# ----> '/interact' setup, note that the decription is not being used here, despite being added
@plugin.command
#@lightbulb.option('gif',
#                  "add a gif to the message?", required=False, default=False,
#                  choices=[hikari.CommandChoice(name='Yes', value=True),
#                           hikari.CommandChoice(name='No', value=False)],
#                  type=bool)
@lightbulb.option('interaction',
                  "type of interaction (More will be added in the future)",
                  required=True,
                  choices=['hug','kiss','boop',],
                  autocomplete=True)
@lightbulb.option('user',
                  'Who would you like to interact with?', required=True)
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommand)
async def interact(ctx):
    user_ran = ctx.author.mention
    user_interact = ctx.options.user
    interaction = ctx.options.interaction
    list = open(f"./plugins/assets/interact/{interaction}_list.txt", "r",encoding='utf-8').read().split("\n")
    list_gif = open(f"./plugins/assets/interact/{interaction}_list_gif.txt", "r",encoding='utf-8').read().split("\n")
    try:
        if ctx.options.gif == True:
            await ctx.respond(f"{list[random.randint(0,len(list))]}\n{list_gif[random.randint(0,len(list_gif))]}".format(user_ran = user_ran,
                                                                                                                         user_interact = user_interact), user_mentions=True)
        else:
            #TODO: Use Tenor API here
            await ctx.respond(f"{list[random.randint(0,len(list))]}".format(user_ran = user_ran, user_interact = user_interact),
                            user_mentions=True)
    except FileNotFoundError:
        await ctx.respond(f"There was an error opening {interaction} interactions...\nThe error has been logged and will be fixed")
        print(f"ERROR!: Where the fuck is the file for {interaction}s?")

#-----------> More complex interactions,
#---------------------------------> /interact violence user:

def load(bot):
    bot.add_plugin(plugin)
