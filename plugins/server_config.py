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

welcome_keys = ['welcome_channel',
                'welcome_txt',
                'welcome_role',
                ]

goodbye_keys = ['goodbye_channel',
                'goodbye_txt',
                ]

ticket_keys = ['ticket_channel',
               'ticket_message',
               'ticket_txt',
               'ticket_create_txt',
               'ticket_num']

misc_keys = ['server_name',
             'mod_role']

# Common functions
# Writes a dictionary to an existing/new json file
async def json_write(ctx: lightbulb.Context,dic):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    for key in dic.keys():
        try:
            if '/r' in dic[key] and 'ticket' not in key:
                dic[key] = dic[key].split('/r')
            
                for x in dic[key]:
                    if x.startswith(' '):
                        index = dic[key].index(x) 
                        dic[key][index] = dic[key][index].replace(" ", "", 1)
        
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

# Deletes a Json's keys from key_list   
async def json_erase(ctx: lightbulb.Context, key_list):
    server = ctx.get_guild().id
    file_location = r"server_save/{server}.json".format(server=server)
    
    if ctx.options.setting == 'ticket':
        channel = await json_get(server,'ticket_channel')
        message = await json_get(server,'ticket_message')
        await ctx.bot.rest.delete_message(channel,message)

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
    
        
async def json_get(server, key):
    try:
        open(f'server_save/{server}.json', 'r', encoding='utf-8')
        
    except FileNotFoundError:
        return
    
    else:
        with open(f'server_save/{server}.json', 'r', encoding='utf-8') as json_file:
            jsn = json.load(json_file)
            
            try:
                return jsn[key]
            
            except KeyError:
                return None

async def config_base(ctx:lightbulb.Context, type):
    message = ctx.options.message
    
    if message.lower() == 'reset':
        erase_list = [f'{type}_channel',f'{type}_txt']
        
        await json_erase(ctx, erase_list)
        return await ctx.respond(f'{type} messsage has been reset')
    
    if message.lower() == 'help':
        return await ctx.respond(f"Here's the syntax for /{type},{help_user_join_leave}")

    member = ctx.author.mention
    channel = ctx.options.channel
    server = ctx.get_guild()
    dict = {f"{type}_channel":channel.id,
            f"{type}_txt":message}
    
    if type == 'welcome':
        if ctx.options.role != None:
            role = ctx.options.role
            dict['welcome_role'] = role.id
        else:
            pass

    if type == 'ticket':
        creation_message = ctx.options.creation_message
        mod_role = ctx.options.mod_role
        dict['ticket_create_txt'] = creation_message
        dict['ticket_num'] = 0
        dict['mod_role'] = mod_role.id
    
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
        channel = await json_get(server, 'ticket_channel')
        message = await json_get(server, 'ticket_message')
        message_txt = await json_get(server, 'ticket_txt')
        view = tickets_system()
        msg = await event.app.rest.edit_message(channel,
                                            message,
                                            message_txt,
                                            components=view,
                                            )
        await view.start(msg)


@plugin.listener(hikari.GuildUpdateEvent)
async def guild_name_update(event: hikari.GuildUpdateEvent):
    guild_name = event.get_guild().name
    await json_write(event,{"server_name": guild_name})

# When a member has joined a guild
@plugin.listener(hikari.MemberCreateEvent)
async def welcome_join(event: hikari.MemberCreateEvent) -> None:
    member = event.member
    server = event.get_guild()
    channel = await json_get(server.id,'welcome_channel')
    txt = await json_get(server.id,'welcome_txt')

    if channel == None or txt == None:
        return
    
    try:
        role = await json_get(event.guild_id, 'welcome_role')
        
    except KeyError:
        pass
    
    else:
        await event.app.rest.add_role_to_member(event.guild_id,member,role)
    
    if isinstance(txt, list):
        txt = random.choice(txt)
    
    await event.app.rest.create_message(channel, txt.format(member=member.mention,server=server.name,count=server.member_count),
                                        user_mentions=True)

# When a member has left the guild       
@plugin.listener(hikari.MemberDeleteEvent)
async def welcome_join(event: hikari.MemberDeleteEvent) -> None:
    member = event.old_member
    server = event.get_guild()
    
    try:
       await json_get(event.guild_id,'goodbye_channel')
        
    except FileNotFoundError or KeyError:
        pass
    
    else:
        channel = await json_get(event.guild_id,'goodbye_channel')
        txt = await json_get(event.guild_id,'goodbye_txt')
        
        if isinstance(txt, list):
            txt = random.choice(txt)
        
        await event.app.rest.create_message(channel, txt.format(member=member.display_name,server=server.name,member_count=server.member_count),
                                      user_mentions=True)

# Commands
# /reset <setting[welcome,goodbye,]
# reset a selected server setting TODO: Maybe add an 'all' selection?
@plugin.command
@lightbulb.option('setting',
                  'choose a setting to reset',
                  required=True,
                  choices=[hikari.CommandChoice(name='welcome',value='welcome'),
                           hikari.CommandChoice(name='goodbye',value='goodbye'),
                           hikari.CommandChoice(name='tickets',value='ticket'),])
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('reset',
                   'reset server settings')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx: lightbulb.Context):
    setting = ctx.options.setting
    erase_list = globals()[f'{setting}_keys']
    
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
    await config_base(ctx, 'welcome')
    
    role = ctx.options.role
    if role != None:
        server = ctx.get_guild()
        channel = await json_get(server.id,'welcome_channel')
        member = ctx.author.mention
        message = await json_get(server.id, 'welcome_txt')
    
        await json_write(ctx,{"welcome_role": role.id})
        if isinstance(message, list):
            message = random.choice(message)
        await ctx.edit_last_response(f"Welcome channel has successfully been set to <#{channel}>\nUser will join with role: <@&{role}>\n{message.format(member=member, server=server.name, count=server.member_count)}", 
                                 user_mentions=False, role_mentions=False)
        
    
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
    await config_base(ctx, 'goodbye')

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
@lightbulb.command('tickets',
                   'set up a tickets channel', 
                   auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def tickets(ctx: lightbulb.Context):
    await config_base(ctx,'ticket')
    server = ctx.get_guild()
    member = ctx.author
    mod = await json_get(server.id,"mod_role")
    channel = await json_get(server.id,"ticket_channel")
    message = await json_get(server.id,"ticket_txt")
    creation_message = await json_get(server.id,"ticket_create_txt")
    
    await ctx.edit_last_response(f"Ticket channel has successfully been set to <#{channel}>\n{message}\n\n{creation_message.format(member=member.mention,mod=f'<@&{mod}>')}", 
                                 user_mentions=False, role_mentions=False)
    
    view = tickets_system()
    message = await ctx.bot.rest.create_message(channel,message, components=view)
    await view.start(message)
    await json_write(ctx,{'ticket_message': message.id})
    

@plugin.command
@lightbulb.command('open-ticket',
                   'open a ticket',
                   auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def openticket(ctx: lightbulb.Context):
    await ctx.respond("You'll be mentioned once your ticket is created", flags=hikari.MessageFlag.EPHEMERAL)
    await ticket_create()
    
# Loads the plugin
def load(bot):
    bot.add_plugin(plugin)
    