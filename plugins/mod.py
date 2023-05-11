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
    #TODO: make responses empheral..
    if ctx.author.id == 592732403546587323:
        server = ctx.get_guild() #TODO: fix user_id: - Value "<@USERID>" is not snowflake.
        ban_reason = ctx.options.reason
        remove_chara = ["<","@",">"]
        user_interact = ctx.options.user
        for x in remove_chara:
            user_interact = str.replace(user_interact,x, "")
        await server.ban(user_interact, reason=ban_reason)
        await ctx.respond(f"{ctx.options.user} was succesfully banned with reason:\n{ban_reason}", '''ephemeral = True''')
    else: #TODO: Remove if statment when code is finished
        await ctx.respond("My creator doesn't trust this command yet, please try another time", '''ephemeral = True''')
    
    
    
    
    


def load(bot):
    bot.add_plugin(plugin)
