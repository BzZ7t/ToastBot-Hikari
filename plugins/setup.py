import json
import os

import hikari
import lightbulb

#from bot import get_json

plugin = lightbulb.Plugin('setup', default_enabled_guilds=1011278408770146374)

async def json_write(ctx, key, key_value, type):
    server = ctx.get_guild().id
    json_file = open(f'server_save/{server}.json', 'a+', encoding='utf-8')
    

    if isinstance(key_value, str) and key_value.lower() == 'reset':
        try:
            jsn.pop(key)
        except FileNotFoundError or KeyError or json.decoder.JSONDecodeError:
            pass
        return await ctx.respond(f"'{type}' settings have been reset")

    with json_file as jsn:
        try:
            fille = json.load(jsn)
            dicc = {key:key_value}
            fille.update(dicc)
        except json.decoder.JSONDecodeError:
            fille = {key:key_value}
        json.dump(fille,jsn, indent=2)

            
    
    
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
    
    await ctx.respond(f"welcome channel will be set to {channel}\n- {message}")
    await json_write(ctx,"welcome_channel",channel.id,'welcome')
    await json_write(ctx,"welcome_txt",message,'welcome')
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
    await json_write(ctx,"goodbye_channel",channel,'goodbye')
    await json_write(ctx,"goodbye_txt",message,'goodbye') 
    await ctx.edit_last_response(f"goodbye channel has successfully been set to {channel}\n- {message.format(user=user)}")


def load(bot):
    bot.add_plugin(plugin)
    