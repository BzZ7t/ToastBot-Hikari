import json
import os

import hikari
import lightbulb

plugin = lightbulb.Plugin('setup')

def get_welcome(ctx):
    server = ctx.get_guild().id
    with open(f'server_save/{server}/welcome.json', 'r', encoding='utf-8') as json_file:
        jsn_welcome = json.load(json_file)
    return jsn_welcome

#TODO: WHY THEGFTGUJRFTURFYUR6YU8FYDSRTHFJFRSTYH
@plugin.listener(hikari.MemberCreateEvent)
async def welcome_join(ctx: lightbulb.context) -> None:
    try:
        file = await get_welcome(ctx)
        await ctx.respond(file['welcome_channel'], file['welcome_txt'])
        
    except FileNotFoundError:
        pass

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
@lightbulb.add_checks(lightbulb.checks.owner_only,#TODO: Remove once finished
                      lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('welcome',
                   'set up a welcome channel') 
@lightbulb.implements(lightbulb.SlashSubCommand)
async def welcome(ctx):
    message = ctx.options.message
    server = ctx.get_guild().id
    channel = ctx.options.channel
    channel_id = channel
    chara_rem = ['<','#','>']
    file = {
        "server_id":server,
        "welcome_channel":channel_id,
        "welcome_txt":message
    }
    newpath = r'/home/mint/Desktop/GithubRepos/ToastBot-Hikari/server_save/{server}'.format(server=server) 
    
    for x in chara_rem:
        channel_id = channel_id.replace(x,'') 
        # Yes its dirty. I'm aware that they may be a command behavour to fix this, no clue what it is tho
        #TODO: Find that shit
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    file_location = open(f'server_save/{server}/welcome.json', 'w', encoding='utf-8')
    with file_location as json_file:
        json.dump(file,json_file, indent=2)
        
    await ctx.respond(f'A welcome channel has been set to {channel}\n{message}')

def load(bot):
    bot.add_plugin(plugin)
    