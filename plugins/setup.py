import json
import os

import hikari
import lightbulb

#from bot import get_json

plugin = lightbulb.Plugin('setup')
"""
async def json_write(ctx, key, key_value, type):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    file_location = open(file_location,"w+", encoding="utf-8")
    
    with file_location:
        if isinstance(key_value, str) and key_value.lower() == 'reset':
            try:
                json_open = json.load(file_location)
                json_open.pop(key)
            except FileNotFoundError or KeyError or json.decoder.JSONDecodeError:
                pass
            return await ctx.respond(f"'{type}' settings have been reset")

        try:
            json_file = json.load(file_location)
            dicc = {key:key_value}
            json_file.update(dicc)
        except json.decoder.JSONDecodeError:
            json_file = {key:key_value}
        json.dump(json_file,file_location, indent=2)
"""

async def json_write(ctx,dictionary,type):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    with open(file_location,"w+", encoding="utf-8") as fs:
        json_file = json.load(fs)
        json.dump(json_file,file_location,indent=2)
    
    
async def json_erase(ctx, key, key_value):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    file_location = open(file_location,"w+", encoding="utf-8")
    
    if isinstance(key_value, str) and key_value.lower() == 'reset':
            try:
                json_open = json.load(file_location)
                json_open.pop(key)
            except FileNotFoundError or KeyError or json.decoder.JSONDecodeError:
                pass
            return await ctx.respond(f"'{type}' settings have been reset")  

#TODO: Simplify how you simplified /interact
@plugin.command
@lightbulb.option('message',
                  'set a message (type "reset" to reset, for mentions and other syntax, type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the welcome channel',
                  hikari.GuildChannel,
                  required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('welcome',
                   'set up a welcome channel') 
@lightbulb.implements(lightbulb.SlashCommand)
async def welcome(ctx):
    user = ctx.author.mention
    message = ctx.options.message
    channel = ctx.options.channel
    
    if message.lower() == 'help':
        return await ctx.respond()
    welcome_dict = {
        "welcome_channel":channel.id,
        "welcome_txt":message
    }
    
    await json_write(ctx,welcome_dict,"welcome")

    await ctx.respond(f"welcome channel will be set to {channel}\n- {message}")
    #await json_write(ctx,"welcome_channel",channel.id,'welcome')
    #await json_write(ctx,"welcome_txt",message,'welcome')
    await ctx.edit_last_response(f"welcome channel has successfully been set to {channel}\n- {message.format(user=user)}")

@plugin.command
@lightbulb.option('message',
                  'set a message (type "reset" to reset, for mentions and other syntax, type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the goodbye channel',
                  hikari.GuildChannel,
                  required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('goodbye',
                   'set up a goodbye channel') 
@lightbulb.implements(lightbulb.SlashCommand)
async def goodbye(ctx):
    user = ctx.author.mention
    message = ctx.options.message
    channel = ctx.options.channel
    
    
    await ctx.respond(f"goodbye channel will be set to {channel}\n- {message}")
    await ctx.edit_last_response(f"goodbye channel has successfully been set to {channel}\n- {message.format(user=user)}")


def load(bot):
    bot.add_plugin(plugin)
    