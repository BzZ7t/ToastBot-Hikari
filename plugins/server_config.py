# imports
import json
import random
import os
import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin('server_config')
plugin.add_checks(lightbulb.guild_only)

# Common variables
help_user_join_leave = '''
`{member}` - mention a user
`{server}` - current name of the server
`{count}` - Number of members in a server

You can also use `/r` to make a list of messages that the bot will randomly choose from
An example of that would be `message1/rmessage2`'''


# Common functions
# Writes a dictionary to an existing/new json file
async def json_write(ctx: lightbulb.Context,dic):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    cmd = ctx.command
    dicsub = dic[cmd.name]
    for key in dicsub.keys():
        try:
            if '/r' in dicsub[key] and 'txt' in key:
                dicsub[key] = dicsub[key].split('/r')
            
                for x in dicsub[key]:
                    if x.startswith(' '):
                        index = dicsub[key].index(x) 
                        dicsub[key][index] = dicsub[key][index].replace(" ", "", 1)
        
        except TypeError:
            pass
            
    try:
        open(file_location,'r+', encoding="utf-8")
    
    except FileNotFoundError or json.decoder.JSONDecodeError:
            with open(file_location,'x', encoding="utf-8") as fs:
                dic['info'] = {}
                dic['info']['name'] = ctx.get_guild().name
                json_file = dic
                json.dump(json_file,fs,indent=2)
                
    else:
        with open(file_location,'r+', encoding="utf-8") as fs:
            json_file = json.load(fs)
            json_file = json_file | dic       
            fs =  open(file_location,'w', encoding="utf-8")
            json.dump(json_file,fs,indent=2)

# Deletes a Json's keys from key_list   
async def json_erase(ctx: lightbulb.Context, server, key, subkey):
    file_location = r"server_save/{server}.json".format(server=server)
    
    if key == 'tickets':
        channel = await json_get(server, key, 'channel')
        message = await json_get(server, key, 'message')
        await ctx.bot.rest.delete_message(channel, message)

    try:
        with open(file_location,'r+', encoding="utf-8") as fs:
            json_file = json.load(fs)
            try:
                if subkey == 'all':
                    del json_file[key]
                else:
                    del json_file[key][subkey]
                
            except KeyError:
                return
                
            fs = open(file_location,'w', encoding="utf-8")
            json.dump(json_file,fs,indent=2)
    
    except FileNotFoundError or KeyError:
        pass
    
        
async def json_get(server, key, subkey):
    try:
        open(f'server_save/{server}.json', 'r', encoding='utf-8')
        
    except FileNotFoundError:
        return
    
    else:
        with open(f'server_save/{server}.json', 'r', encoding='utf-8') as json_file:
            jsn = json.load(json_file)
            try:
                if subkey == 'all':
                    return jsn[key]  
                else:
                    return jsn[key][subkey]
            
            except KeyError:
                return None

async def config_base(ctx:lightbulb.Context, type):  # Unsure if will keep, TODO: If kept, rewrite for new system
    server = ctx.get_guild()
    channel = ctx.options.channel
    message = ctx.options.message
    member = ctx.author.mention
    
    dict = {
        type:{
            'channel': channel.id,
            "txt":message
            }}
    
    if type == 'welcome':
        if ctx.options.role != None:
            role = ctx.options.role
            dict[type]['role'] = role.id
        else:
            pass

    if type == 'ticket':
        creation_message = ctx.options.creation_message
        mod_role = ctx.options.mod_role
        dict[type]['create_txt'] = creation_message
        dict[type]['num'] = 0
        dict[type]['mod_role'] = mod_role.id
    
    await ctx.respond(f"{type} channel will be set to {channel}\n{message}")
    await json_write(ctx,dict)
    channel = await json_get(server.id, f"{type}_channel")
    message = await json_get(server.id, f"{type}_txt")
    if isinstance(message, list):
        message = random.choice(message)

    await ctx.edit_last_response(f"{type} channel has successfully been set to <#{channel}>\n{message.format(member=member, server=server.name, count=server.member_count)}", 
                                 user_mentions=False)

async def ticket_create(ctx: lightbulb.Context):
    server = ctx.get_guild()
    member = ctx.author
    mod = await json_get(server.id,"mod_role")
    message = await json_get(server.id,"ticket_create_txt")
    number = await json_get(server.id, "ticket_num")
    number =+ 1
    channel_name = f'Ticket #{number}'
    
    channel_id = await ctx.get_channel().app.rest.create_guild_text_channel(server.id,
                                                                            channel_name,
                                                                            )
    
    # Very strange issue with edit_channel(), Error leads to following:
    
    # File "/home/mint/.local/lib/python3.10/site-packages/hikari/internal/data_binding.py", line 356, in put_array
    # self[key] = [conversion(value) for value in values]
    # TypeError: 'PermissionOverwrite' object is not iterable
    
    # TODO: Possible Hikari bug, if not, figure  out what you did wrong
    
    perms = (hikari.Permissions.VIEW_CHANNEL |
            hikari.Permissions.SEND_MESSAGES |
            hikari.Permissions.READ_MESSAGE_HISTORY)
    

    await ctx.bot.rest.edit_channel(channel_id,
                                    permission_overwrites=hikari.PermissionOverwrite(
                                        id=server.id,
                                        type=hikari.PermissionOverwriteType.ROLE,
                                        deny=perms,
                                        
                                        ),
                                    )
    
    await ctx.bot.rest.edit_channel(channel_id, 
                                    permission_overwrites=hikari.PermissionOverwrite(
                                        id=member,
                                        type=hikari.PermissionOverwriteType.MEMBER,
                                        allow=perms
                                        )
                                    )
    
    await ctx.bot.rest.edit_channel(channel_id, 
                                    permission_overwrites=hikari.PermissionOverwrite(
                                        id=mod,
                                        type=hikari.PermissionOverwriteType.ROLE,
                                        allow=perms
                                        )
                                    )
    
    await ctx.bot.rest.create_message(channel_id,message.format(member=member.mention, mod=f'<@&{mod}>'),
                                    user_mentions=True,role_mentions=True)
    await json_write(ctx,{"ticket_num": number})

# Common classes
class tickets_system(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)  # Setting timeout to None

    @miru.button(label='Create a Ticket', style=hikari.ButtonStyle.PRIMARY)
    async def btn_create_ticket(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ticket_create(ctx)
        

# Listeners
# Listens to a server name change TODO: unsure is this is its only function, docs says "Event fired when an existing guild is updated" which is so vague
@plugin.listener(hikari.StartedEvent)
async def persistant_miru(event: hikari.StartedEvent):
    for path in os.listdir('server_save'):
        server = path.split('.')[0]
        tickets = await json_get(server, 'tickets', 'all')
        if tickets == None:
            continue
        
        channel = await json_get(server, 'tickets', 'channel')
        message = await json_get(server, 'tickets', 'message')
        txt = await json_get(server, 'tickets', 'txt')
        view = tickets_system()
        msg = await event.app.rest.edit_message(channel, message, txt,
                                            components=view)
        await view.start(msg)

@plugin.listener(hikari.GuildUpdateEvent)
async def guild_name_update(event: hikari.GuildUpdateEvent):
    guild_name = event.get_guild().name
    save = {'info': {
        'server_name': guild_name,
    }}
    await json_write(event, save)

# When a member has joined a guild
@plugin.listener(hikari.MemberCreateEvent)
async def welcome_join(event: hikari.MemberCreateEvent) -> None:
    server = event.get_guild()
    welcome = await json_get(server.id, 'welcome', 'all')
    if welcome == None:
        return
    
    role = await json_get(server.id, 'welcome', 'role')
    member = event.member
    channel = await json_get(server.id,'welcome', 'channel')
    txt = await json_get(server.id,'welcome', 'txt')
    
    if role != None:
        await event.app.rest.add_role_to_member(event.guild_id,member,role)
    
    if isinstance(txt, list):
        txt = random.choice(txt)
    
    txt = txt.format(member=member.mention,server=server.name,count=server.member_count)
    await event.app.rest.create_message(channel, txt, user_mentions=True)

# When a member has left the guild       
@plugin.listener(hikari.MemberDeleteEvent)
async def goodbye_left(event: hikari.MemberDeleteEvent) -> None:
    server = event.get_guild()
    goodbye = await json_get(server.id, 'goodbye', 'all')
    if goodbye == None:
        return
    
    member = event.old_member
    channel = await json_get(server.id,'goodbye', 'channel')
    txt = await json_get(server.id,'goodbye', 'txt')
    
    if isinstance(txt, list):
        txt = random.choice(txt)
    
    txt = txt.format(member=member.mention,server=server.name,count=server.member_count)
    await event.app.rest.create_message(channel, txt, user_mentions=True)


@plugin.listener(hikari.MessageCreateEvent)
async def level_xp(event: hikari.MessageCreateEvent):
    if event.is_bot:
        return
    
    


# Commands
# /reset <setting[welcome,goodbye,]
# reset a selected server setting TODO: Maybe add an 'all' selection?
@plugin.command
@lightbulb.option('setting',
                  'choose a setting to reset',
                  required=True,
                  choices=['welcome',
                           'goodbye',
                           'tickets',
                           'levels',])
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('reset',
                   'reset server settings')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx: lightbulb.Context):
    server = ctx.get_guild()
    setting = ctx.options.setting
    
    await json_erase(ctx, server.id, setting, 'all')
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
    # await config_base(ctx, 'welcome')
    server = ctx.get_guild()
    channel = ctx.options.channel
    role = ctx.options.role
    member = ctx.author
    txt = ctx.options.message
    cmd = ctx.command
    
    save = {
        cmd.name:{
            'channel': channel.id,
            'role': role.id,
            'txt': txt,
    }}
    
    
    await ctx.respond(f'The {cmd.name} settings will be set to the following,\nChannel: {channel.name}\nRole on join: {role.name}\nmessage:\n{txt}')
    await json_write(ctx,save)
    
    print(f'{server}: {server.id}')
    channel = await json_get(server.id, cmd.name, 'channel')
    role = await json_get(server.id, cmd.name, 'role')
    txt = await json_get(server.id, cmd.name, 'txt')

    response = await ctx.edit_last_response(f'The levels have been set to the following,\n\nChannel: <#{channel}>\nRole on join: <@&{role}>\nmessage:\n')
    
    if isinstance(txt, list):
        total_txt = 0
        for x in txt:
            x = x.format(user=member.mention,server=server.name,count=server.member_count)
            ctx.bot.rest.create_message(response.channel_id, x, 
                                        user_mentions=True,
                                        role_mentions=False)
            total_txt =+ 1

        await ctx.bot.rest.create_message(response.channel_id, f'\nI will randomly choose one of the {total_txt} messages when a user joins')
    
    else:
        #txt = txt.format(user=member.mention,server=server.name,count=server.member_count)
        await ctx.bot.rest.create_message(response.channel_id, txt.format(user=member.mention,server=server.name,count=server.member_count), 
                                    user_mentions=True,
                                    role_mentions=False)
        
    
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
    #await config_base(ctx, 'goodbye')
    server = ctx.get_guild()
    channel = ctx.options.channel
    member = ctx.author
    txt = ctx.options.message
    cmd = ctx.command
    
    save = {
        cmd.name:{
            'channel': channel.id,
            'txt': txt,
            }}
    
    
    await ctx.respond(f'The {cmd.name} settings will be set to the following,\nChannel: {channel.name}\nmessage:\n{txt}')
    await json_write(ctx,save)
    
    channel = await json_get(server.id, cmd.name, 'channel')
    txt = await json_get(server.id, cmd.name, 'txt')

    response = await ctx.edit_last_response(f'The {cmd.name} settings have been set to the following,\n\nChannel: <#{channel}>\nMessage/s:')
    
    if isinstance(txt, list):
        total_txt = 0
        for x in txt:
            x = x.format(user=member.mention,server=server.name,count=server.member_count)
            ctx.bot.rest.create_message(response.channel_id, x, 
                                        user_mentions=True,
                                        role_mentions=False)
            total_txt =+ 1

        await ctx.bot.rest.create_message(response.channel_id, f'\nI will randomly choose one of the {total_txt} messages when a user leaves')
    
    else:
        txt = txt.format(user=member.mention,server=server.name,count=server.member_count)
        await ctx.bot.rest.create_message(response.channel_id, txt, 
                                    user_mentions=True,
                                    role_mentions=False)
            
@plugin.command
@lightbulb.option('creation_message',
                  'The message sent once a user has created a ticket',
                  required=False,
                  default='{member} a moderator will be with you shortly\n{mod}')
@lightbulb.option('message',
                  'add your own message to the tickets channel',
                  required=False,
                  default='Any mod related issues?\nPress the button below to create a ticket!')
@lightbulb.option('mod_role',
                  'allow moderators to see and type in the ticket',
                  hikari.Role,
                  required=True)
@lightbulb.option('channel',
                  'set the tickets channel',
                  hikari.TextableGuildChannel,
                  required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('tickets',
                   'set up a tickets channel', 
                   auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def tickets(ctx: lightbulb.Context):
    # await config_base(ctx,'ticket')
    server = ctx.get_guild()
    mod = ctx.options.mod_role
    member = ctx.author
    channel = ctx.options.channel
    txt = ctx.options.message
    creation_txt = ctx.options.creation_message
    cmd = ctx.command
    
    await ctx.respond(f'The {cmd.name} settings will be set to the following,\nChannel: {channel.name}\nMessage:\n{txt}\nMessage when ticket is created:\n{creation_txt}')
    
    view = tickets_system()
    message = await ctx.bot.rest.create_message(channel,txt, components=view)
    await view.start(message)
    save = {cmd.name:{
        'mod': mod.id,
        'channel': channel.id,
        'message': message.id,
        'txt': txt,
        'creation_txt': creation_txt
    }}
    
    await json_write(ctx, save)
    mod = await json_get(server.id, cmd.name, 'mod')
    channel = await json_get(server.id, cmd.name, 'channel')
    txt = await json_get(server.id, cmd.name, 'txt')
    creation_txt = await json_get(server.id, cmd.name, 'creation_txt')
    
    response = await ctx.edit_last_response(f'The {cmd.name} settings has been set to the following,\nChannel: <#{channel}>\nMessage:\n{txt}\nMessage/s when ticket is created:\n')
    
    if isinstance(txt, list):
        total_txt = 0
        for x in txt:
            x = x.format(user=member.mention,server=server.name,count=server.member_count)
            ctx.bot.rest.create_message(response.channel_id, x, 
                                        user_mentions=True,
                                        role_mentions=False)
            total_txt =+ 1

        await ctx.bot.rest.create_message(response.channel_id, f'\nI will randomly choose one of the {total_txt} messages when a user creates a ticket')
    
    else:
        txt = txt.format(user=member.mention,server=server.name,count=server.member_count)
        await ctx.bot.rest.create_message(response.channel_id, txt, 
                                    user_mentions=True,
                                    role_mentions=False)
    

@plugin.command
@lightbulb.command('open-ticket',
                   'open a ticket',
                   auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def openticket(ctx: lightbulb.Context):
    await ctx.respond("You'll be mentioned once your ticket is created", flags=hikari.MessageFlag.EPHEMERAL)
    await ticket_create()


@plugin.command
@lightbulb.option('cooldown',
                  'The the cooldown of xp given with each message in seconds (default is 60)',
                  required=False,
                  default=15)
@lightbulb.option('maximum',
                  'The maximum xp given to a user per message (default is 40)',
                  required=False,
                  default=40)
@lightbulb.option('minimum',
                  'The minumum xp given to a user per message (default is 15)',
                  required=False,
                  default=15)
@lightbulb.option('enabled',
                  'Enable or disable leveling',
                  required=False,
                  default=None,
                  choices=[hikari.CommandChoice(name='Yes', value='True'),
                           hikari.CommandChoice(name='No', value='False')
                           ])
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('levels',
                   "configure the server's leveling system")
@lightbulb.implements(lightbulb.SlashCommand)
async def levels(ctx: lightbulb.Context):
    server = ctx.get_guild()
    enabled = ctx.options.enabled
    min_xp = ctx.options.minimum
    max_xp = ctx.options.maximum
    cooldown = ctx.options.cooldown
    cmd = ctx.command
    
    if enabled == None:
        enabled = await json_get(server.id, cmd.name, 'enabled')
    else:
        enabled = bool(enabled)
    
    save = {
        cmd.name:{
            'enabled': enabled,
            'min_xp': min_xp,
            'max_xp': max_xp,
            'cooldown': cooldown
    }}
    
    
    await ctx.respond(f'The {cmd.name} settings will be set to the following,\nEnabled: {enabled}\nMinimum XP: {min_xp}\nMaximum XP: {max_xp}\nXP Cooldown: {cooldown}')
    await json_write(ctx,save)
    enabled = await json_get(server.id, cmd.name, 'enabled')
    min_xp = await json_get(server.id, cmd.name, 'min_xp')
    max_xp = await json_get(server.id, cmd.name, 'max_xp')
    cooldown = await json_get(server.id, cmd.name, 'cooldown')

    await ctx.edit_last_response(f'The {cmd.name} settings have been set to the following,\nEnabled: `{enabled}`\nMinimum XP: `{min_xp}`\nMaximum XP: `{max_xp}`\nXP Cooldown: `{cooldown}`')

# Loads the plugin
def load(bot):
    bot.add_plugin(plugin)
    