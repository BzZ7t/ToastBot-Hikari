# Imports
import asyncio
import random
import time

import hikari
import lightbulb

plugin = lightbulb.Plugin("mod")


# '/mod' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("mod",
                  "Moderation tools for the Mod Team")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def mod():
    pass

# /mod ban <user> <reason>
# ban a member from the server
@mod.child
@lightbulb.add_cooldown(3.0, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
                      lightbulb.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("reason",
                  "What is the reason for ban?",
                  required=False,
                  default='No reason given')
@lightbulb.option("user",
                  "Who is the user you would like to ban?",
                  hikari.Member,
                  required=True)
@lightbulb.command('ban',
                   'ban a member from the server')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ban(ctx: lightbulb.Context):
    server = ctx.get_guild() 
    reason = f"{ctx.options.reason}\nBanned by {ctx.author.global_name} with ToastBot"
    user = ctx.options.user
    
    
    await server.ban(user.id, reason=reason) 
    await ctx.respond(f"{user} was succesfully banned with reason:\n`{reason}`", flags=hikari.MessageFlag.EPHEMERAL)
    
# /mod kick <user> <reason>
# kick a member from the server
@mod.child
@lightbulb.add_cooldown(3.0, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
                      lightbulb.bot_has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("reason",
                  "What is the reason for kick?", required=False,
                  default='No reason given')
@lightbulb.option("user",
                  "Who is the user you would like to kick?",
                  hikari.Member,
                  required=True)
@lightbulb.command('kick',
                   'kick a member from the server')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kick(ctx: lightbulb.Context):
    server = ctx.get_guild()
    reason = f"{ctx.options.reason}\n Kicked by {ctx.author.global_name} with ToastBot"
    user = ctx.options.user
    
    await server.kick(user.id, reason=reason)
    await ctx.respond(f"{user} was succesfully kicked with reason:\n`{reason}`", flags=hikari.MessageFlag.EPHEMERAL)
    
    
    
    

# Loading the bot
def load(bot):
    bot.add_plugin(plugin)
