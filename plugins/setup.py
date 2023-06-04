import json
import os

import hikari
import lightbulb

#from bot import get_json

plugin = lightbulb.Plugin('setup')


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
    server = ctx.get_guild().id
    channel = ctx.options.channel
    file = {
        "welcome_channel_id":channel.id,
        "welcome_txt":message,
        }
    newpath = r'/home/mint/Desktop/GithubRepos/ToastBot-Hikari/server_save/{server}'.format(server=server) 
    
    
    if message.lower() == 'help':
        return await ctx.respond('Here is the syntax for the welcome command;\n{user} - mentions the user')
    
    if message.lower() == 'reset':
        try:
            os.remove(f"server_save/{server}/welcome.json")
        except FileNotFoundError:
            pass
        return await ctx.respond("'welcome' settings have been reset")
    
    await ctx.respond(f'A welcome channel has been set to {channel.mention}\nwith message:\n{message.format(user=user)}')
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    file_location = open(f'server_save/{server}/welcome.json', 'w', encoding='utf-8')
    with file_location as json_file:
        json.dump(file,json_file, indent=2)
        
    
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
    server = ctx.get_guild().id
    channel = ctx.options.channel
    file = {
        "goodbye_channel_id":channel.id,
        "goodbye_txt":message,
        }
    newpath = r'/home/mint/Desktop/GithubRepos/ToastBot-Hikari/server_save/{server}'.format(server=server) 
    
    if message.lower() == 'help':
        return await ctx.respond('Here is the syntax for the goodbye command;\n{user} - mentions the user')
    
    if message.lower() == 'reset':
        try:
            os.remove(f"server_save/{server}/goodbye.json")
        except FileNotFoundError:
            pass
        return await ctx.respond("'goodbye' settings have been reset")
    
    await ctx.respond(f'A goodbye channel has been set to {channel.mention}\nwith message:\n{message.format(user=user)}')

    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    file_location = open(f'server_save/{server}/goodbye.json', 'w', encoding='utf-8')
    with file_location as json_file:
        json.dump(file,json_file, indent=2)
        

def load(bot):
    bot.add_plugin(plugin)
    