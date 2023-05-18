#-------------> Imports
import asyncio
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("mod")

#----> '/fun' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("mod",
                  "Moderation tools for the Mod Team")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def mod(ctx):
    pass

@mod.child
@lightbulb.add_cooldown(3.0, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
                      lightbulb.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("reason",
                  "What is the reason for ban?", required=False,
                  default='No reason given')
@lightbulb.option("user",
                  "Who is the user you would like to ban?",
                  required=True)
@lightbulb.command('ban',
                   'ban a member from the server')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ban(ctx):
    server = ctx.get_guild() 
    reason = ctx.options.reason
    remove_chara = ["<","@",">"]
    user_interact = ctx.options.user
    
    for x in remove_chara: 
        user_interact = str.replace(user_interact,x, "")
    await server.ban(user_interact, reason=reason)
    await ctx.respond(f"{ctx.options.user} was succesfully banned with reason:\n`{reason}`", flags=hikari.MessageFlag.EPHEMERAL)
    

@mod.child
@lightbulb.add_cooldown(3.0, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
                      lightbulb.bot_has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("reason",
                  "What is the reason for kick?", required=False,
                  default=f'No reason given')
@lightbulb.option("user",
                  "Who is the user you would like to kick?",
                  required=True)
@lightbulb.command('kick',
                   'kick a member from the server')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kick(ctx):
    server = ctx.get_guild()
    reason = f"{ctx.options.reason}"
    remove_chara = ["<","@",">"]
    user_interact = ctx.options.user
    
    for x in remove_chara: 
        user_interact = str.replace(user_interact,x, "")
    await server.kick(user_interact, reason=reason)
    await ctx.respond(f"{ctx.options.user} was succesfully kicked with reason:\n`{reason}`", flags=hikari.MessageFlag.EPHEMERAL)
    
    
    
    


def load(bot):
    bot.add_plugin(plugin)
