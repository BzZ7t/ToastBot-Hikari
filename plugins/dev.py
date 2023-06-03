# The commands here will not be in the final runing of the bot
# Some commands are either not funtioning or are just for the sily
import asyncio
import os
import random
import time
from io import BytesIO

import hikari
import lightbulb
import miru
import PIL 
import requests
from PIL import Image

plugin = lightbulb.Plugin("dev", default_enabled_guilds=1011278408770146374)

#why did I make a /test command? isn't thats what /ping is for?
    
#/cute-checkrr command for playing around with Kohvi hehe
@plugin.command
@lightbulb.command('cute-checkrr',
                   'checks if you cute')
@lightbulb.implements(lightbulb.SlashCommand)
async def cute(ctx):
    user_ran = f"<@{ctx.author.id}>"
    if ctx.author.id == 1103121815838146684:
        await ctx.respond(f'Cmon {user_ran} we both know you are~')
    elif ctx.author.id == 592732403546587323:
        await ctx.respond(f'ewew nasty {user_ran} you nasty >~>')
    else:
        print("banana")
    
#optimisaiton of the error handler that is in bot.py however it doesn't work
#it correctly catches the error but responds with all of the contents of error_dict=
@plugin.listener(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    #TODO: Find 'missing_options' proper syntax pls Zed
    error_dict = {
        lightbulb.errors.CommandNotFound:None,
        lightbulb.errors.NotEnoughArguments:await event.context.respond("Some arguments are missing: "+", ".join(event.exception.missing_options)),
        #                                                                flags=hikari.MessageFlag.EPHEMERAL),
        lightbulb.errors.CommandIsOnCooldown:await event.context.respond(f"Hey! You gotta wait a bit before you do this command again!\nPlease wait a few second before trying again.",
                                                                        flags=hikari.MessageFlag.EPHEMERAL),
        lightbulb.errors.MissingRequiredPermission:await event.context.respond("Hey! You don't have the permissions to do this here!",
                                                                            flags=hikari.MessageFlag.EPHEMERAL),
        lightbulb.errors.BotMissingRequiredPermission:await event.context.respond("Uhhh.. No can do...\nI don't have the permissions to do that ^^'",
                                                                                flags=hikari.MessageFlag.EPHEMERAL),
        lightbulb.errors.CheckFailure: None
        }

    if isinstance(event.exception.__cause__, hikari.ForbiddenError):
        await event.context.respond("Something is missing perms or missed ids...",
                                    flags=hikari.MessageFlag.EPHEMERAL)
        raise event.exception

    else:
        try:
            print(event.exception)
            return error_dict[event.exception]
        except KeyError:
            await event.context.respond("Ohhh no.. some error has happend and I'm not sure what it is o.o\nit might be something the following:\n - The command no workie.\n - The command is under maintenance (Goddamit Zed).\n - You didn't use the command correctly (/help to view command stuffs)",
                                        flags=hikari.MessageFlag.EPHEMERAL)
            raise event.exception
        

#supposted be to /interact violence but here is /violence. 
#currently doesn't work...
#deleted due to be rewritten in the future or be kept scrapped entirely
#it would allow the user to 'attack' other users 
#the bot would chose a random response
#randomly, the other user would have a chance to dodge
#if the other user doesn't dodge in time, they fail to dodge
#I even asked chatGPT for this shit, what the hell happend to its now watered down AI?
#Bad users fucked it as always when somthing gets popular

#Command originally sent as a simple link, but because of how discord
#works, it just showed a random image each person because the link gives
#a random image blah blah blah somthing technical
#Tried storing the file in a variable first before sending but I have no fucking clue
#how to from these libaries 

#HAHAHHAHA WE FUCKING FIXED IT (With the help of Jack)


def load(bot):
    bot.add_plugin(plugin)