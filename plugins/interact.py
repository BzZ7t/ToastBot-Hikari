import random

import hikari
import lightbulb

plugin = lightbulb.Plugin("interact")

#----> '/fun' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def interact(ctx):
    pass

@interact.child
@lightbulb.command('violence',
                   "today you chose violence")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def violence(ctx):
    #TODO: User ID needed
    user_ran = "[user_ran]"
    user_hurt = "[user_hurt]"

    action = [f"{user_ran} decided to throw a stone at {user_hurt}",]
    action_end = [f"{user_ran} gave {user_hurt} a concussion",]
    action_dodged = [f"{user_hurt} dodged {user_ran}'s rock"]
    action_randm = random.randint(0,len(action))
    dodge_randm = [random.randint(0,2)]

    await ctx.respond(action[action_randm])

    if dodge_randm == 1:
        await ctx.respond(f"{user_hurt} you have a chance to dodge it!\nquick! respond with 'dodge' to dodge the attack!")
        #TODO: Listen to message for "dodge" from user_hurt
        dodge_result = "dodge"
        if dodge_result == "dodge":
            await ctx.respond(action_dodged[action_randm])
        else:
            await ctx.respond("You failed to dodge ;-;")
            await ctx.respond(action_end[action_randm])
    else:
        await ctx.respond("they're not able to dodge this time")
        await ctx.respond(action_end[action_randm])
        
def load(bot):
    bot.add_plugin(plugin)