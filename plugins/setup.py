import json
import os

import hikari
import lightbulb

plugin = lightbulb.Plugin('setup')

@plugin.command
@lightbulb.command('setup',
                   'list of setup stuff')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def setup():
    pass

@plugin.command
@lightbulb.option('message',
                  'set a message (type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the welcome channel',
                  required=True)
@lightbulb.command('welcome',
                   'set up a welcome channel') 
@lightbulb.implements(lightbulb.SlashCommand)
async def welcome(ctx):
    message = ctx.options.message
    server = ctx.get_guild().id
    channel = ctx.options.channel
    channel_id = channel
    chara_rem = ['<','#','>']
    for x in chara_rem:
        channel_id = channel_id.replace(x,'') 
        # Yes its dirty. I'm aware that they may be a command behavour to fix this, no clue what it is tho
    file = {"server_id":f"{server}",
            "welcome_channel":f"{channel_id}",
            "welcome_txt":f"{message}"}
    jsn_info = json.dumps(file)
    newpath = r'/home/mint/Desktop/GithubRepos/ToastBot-Hikari/server_save/{server}'.format(server=server) 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    file = open(f'server_save/{server}/welcome.json', 'w', encoding='utf-8')
    with file as json_file:
        json.dump(jsn_info,json_file)
        
    await ctx.respond(f'A welcome channel has been set to {channel}\n{message}')

def load(bot):
    bot.add_plugin(plugin)
    