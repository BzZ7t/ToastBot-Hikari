# imports
import json

import os
import hikari
import lightbulb

# Common variables
plugin = lightbulb.Plugin('setup')
help_user_join_leave = '''
`{member}` - mention a member
`{server}` - current name of the server

You can also use `,` to make a list of messages that the bot will randomly choose from
An example of that would be `message1+message2`'''

# Common functions
# Writes a dictionary to an existing/new json file
async def json_write(ctx: lightbulb.Context,dic):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    for key in dic.keys():
        try:
            if '+' in dic[key]:
                dic[key] = dic[key].split('+')
        
        except TypeError:    
            pass
            
    try:
        open(file_location,'r+', encoding="utf-8")
    
    except FileNotFoundError or json.decoder.JSONDecodeError:
            try:
                os.mkdir(r'server_save/')
            
            except FileExistsError:
                pass
            
            with open(file_location,'x', encoding="utf-8") as fs:
                dic['server_name'] = ctx.get_guild().name
                json_file = dic
                json.dump(json_file,fs,indent=2)
                
    else:
        with open(file_location,'r+', encoding="utf-8") as fs:
            json_file = json.load(fs)
            json_file = json_file | dic       
            fs =  open(file_location,'w', encoding="utf-8")
            json.dump(json_file,fs,indent=2)

# Deletes a Json's keys from key_list   
async def json_erase(ctx: lightbulb.Context, key_list):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    
    try:
        with open(file_location,'r+', encoding="utf-8") as fs:
            json_file = json.load(fs)
            
            for x in key_list:  # This is fucking jank, TODO: Make this not jank
                try:
                    del json_file[x]
                
                except KeyError:
                    return
                
            fs = open(file_location,'w', encoding="utf-8")
            json.dump(json_file,fs,indent=2)
    
    except FileNotFoundError or json.decoder.JSONDecodeError or KeyError:
        pass
    
async def get_json(server, key):
    with open(f'server_save/{server}.json', 'r', encoding='utf-8') as json_file:
        jsn = json.load(json_file)
    return jsn[key]


# Listeners 
# Listens to a server name change TODO: unsure of this, please check that it does this
@plugin.listener(hikari.GuildUpdateEvent)
async def guild_name_update(event: hikari.GuildUpdateEvent):
    guild_name = event.get_guild().name
    await json_write(event,{"server_name": guild_name})

# Commands
# /reset <setting[welcome,goodbye,]
# reset a selected server setting TODO: Maybe add an 'all' selection?
@plugin.command
@lightbulb.option('setting',
                  'choose a setting to reset',
                  required=True,
                  choices=['welcome',
                           'goodbye'])
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('reset',
                   'reset server settings')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx: lightbulb.Context):
    setting = ctx.options.setting
    erase_list = [f'{setting}_channel',
                  f'{setting}_txt',
                  f'{setting}_role']
    await json_erase(ctx, erase_list)
    await ctx.respond(f'{setting} setting has been reset')
    

#TODO: Simplify how you simplified /interact
# /welcome <channel> <message>
# set up a welcome channel
@plugin.command
@lightbulb.option('role',
                  'add a role when user joins?',
                  hikari.Role,
                  required=False,
                  default=None)
@lightbulb.option('message',
                  'set a message (type "reset" to reset, for mentions and other syntax, type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the welcome channel',
                  hikari.TextableGuildChannel,
                  required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('welcome',
                   'set up a welcome channel') 
@lightbulb.implements(lightbulb.SlashCommand)
async def welcome(ctx: lightbulb.Context):
    message = ctx.options.message
    
    if message.lower() == 'reset':
        erase_list = ['welcome_channel','welcome_txt']
        
        await json_erase(ctx, erase_list)
        return await ctx.respond('welcome messsage has been reset')
    
    if message.lower() == 'help':
        return await ctx.respond("Here's the syntax for /welcome,"+help_user_join_leave)

    user = ctx.author.mention
    channel = ctx.options.channel
    dict = {"welcome_channel":channel.id,
            "welcome_txt":message}
    role = ctx.options.role
    
    if role != None:
        dict = {"welcome_channel":channel.id,
            "welcome_txt":message,
            "welcome_role": role.id}
    
    await ctx.respond(f"welcome channel will be set to {channel}\n- {message}")
    await json_write(ctx,dict)
    await ctx.edit_last_response(f"welcome channel has successfully been set to {channel.mention}\n- {message.format(user=user,server=ctx.get_guild().name)}", 
                                 user_mentions=False)

# /goodbye <channel> <message>
# set up a goodbye channel
@plugin.command
@lightbulb.option('message',
                  'set a message (type "reset" to reset, for mentions and other syntax, type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the goodbye channel',
                  hikari.TextableGuildChannel,
                  required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('goodbye',
                   'set up a goodbye channel') 
@lightbulb.implements(lightbulb.SlashCommand)
async def goodbye(ctx: lightbulb.Context):
    message = ctx.options.message
    
    if message.lower() == 'reset':
        erase_list = ['goodbye_channel','goodbye_txt']
        
        await json_erase(ctx, erase_list)
        return await ctx.respond('goodbye messsage has been reset')
    
    if message.lower() == 'help':
        return await ctx.respond()
    
    user = ctx.author.mention
    channel = ctx.options.channel
    dict = {
        "goodbye_channel":channel.id,
        "goodbye_txt":message
    }
    
    await ctx.respond(f"goodbye channel will be set to {channel}\n- {message}")    
    await json_write(ctx,dict)
    await ctx.edit_last_response(f"goodbye channel has successfully been set to {channel.mention}\n- {message.format(user=user,server=ctx.get_guild().name)}",
                                 user_mentions = False)

# Loads the plugin
def load(bot):
    bot.add_plugin(plugin)
    