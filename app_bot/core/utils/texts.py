from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.utils.i18n import gettext

# i18n function
def _(text: str, **kwargs):
    return gettext(text).format(**kwargs)


# create individual commands menu for users, depends on their status
async def set_user_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(
            command='start',
            description=_('START_COMMAND')
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=scope)


async def set_admin_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(
            command='start',
            description=_('START_COMMAND')
        ),
    ]


    await bot.set_my_commands(commands=commands, scope=scope)
