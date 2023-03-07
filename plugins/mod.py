#-------------> Imports
import hikari
import lightbulb

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
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("reason",
                  " (Optional) What is the reason for ban?")
@lightbulb.option("user",
                  "Who is the user you would like to ban?")
@lightbulb.command('ban',
                   'ban a member from the server')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ban(ctx):
    server = ctx.get_guild() #TODO: fix user_id: - Value "<@USERID>" is not snowflake.
    await server.ban(ctx.options.user, reason=ctx.options.reason)
    
    
    
    
    


def load(bot):
    bot.add_plugin(plugin)
