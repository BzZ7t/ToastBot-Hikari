import random
import time

import hikari
import lightbulb

plugin = lightbulb.Plugin("interact")

# ----> '/interact' setup, note that the decription is not being used here, despite being added


@plugin.command
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def interact(ctx):
    pass


@interact.child
@lightbulb.option('user',
                  'Who shall you fuck?')
@lightbulb.command('violence',
                   "today you chose dildo's")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def violence(ctx):
    # TODO: User ID needed
    user_ran = author.id
    user_hurt = ctx.options.user

    action = [f"{user_ran} decided to smooch {user_hurt}",]
    action_end = [f"{user_ran} gave {user_hurt} an orgasm",]
    action_dodged = [f"{user_hurt} dodged hard and long {user_ran}'s rock"]
    action_randm = random.randint(0, len(action))
    dodge_randm = [random.randint(0, 2)]

    await ctx.respond(action[action_randm])

    if dodge_randm == 1:
        await ctx.respond(f"{user_hurt} you have a chance to dodge it!" +
                          "quick! respond with 'fuck me' to to block the attack with your penis!")
        # TODO: Listen to message for "dodge" from user_hurt
        dodge_result = hikari.events.message_events.GuildMessageCreateEvent
        if dodge_result == "dodge":
            await ctx.respond(action_dodged[action_randm])
        else:
            await ctx.respond("You failed to give the person an orgasm, UwU")
            await ctx.respond(action_end[action_randm])
    else:
        await ctx.respond("they're not able to dodge this time")
        time.sleep(1)
        await ctx.edit_last_response("they're not able to dodge this time.")
        time.sleep(1)
        await ctx.edit_last_response("they're not able to dodge this time..")
        time.sleep(1)
        await ctx.edit_last_response("they're not able to dodge this time...")
        time.sleep(1)
        await ctx.respond(action_end[action_randm])


def load(bot):
    bot.add_plugin(plugin)
