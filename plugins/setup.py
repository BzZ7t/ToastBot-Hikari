import json

import hikari
import lightbulb

#from bot import get_json

plugin = lightbulb.Plugin('setup')


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
    
async def json_erase(ctx, key_list):
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
    

#TODO: Simplify how you simplified /interact
@plugin.command
@lightbulb.option('message',
                  'set a message (type "reset" to reset, for mentions and other syntax, type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the welcome channel',
                  hikari.GuildTextChannel,
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
        return await ctx.respond("`halp`")

    user = ctx.author.mention
    channel = ctx.options.channel
    dict = {"welcome_channel":channel.id,
            "welcome_txt":message}
    
    await ctx.respond(f"welcome channel will be set to {channel}\n- {message}")
    await json_write(ctx,dict)
    await ctx.edit_last_response(f"welcome channel has successfully been set to {channel.mention}\n- {message.format(user=user,server=ctx.get_guild().name)}", 
                                 user_mentions=False)

@plugin.command
@lightbulb.option('message',
                  'set a message (type "reset" to reset, for mentions and other syntax, type "help" for more details)',
                  required=True)
@lightbulb.option('channel',
                  'set the goodbye channel',
                  hikari.GuildTextChannel,
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


def load(bot):
    bot.add_plugin(plugin)
    