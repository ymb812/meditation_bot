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
            command='cancel',
            description=_('CANCEL_COMMAND')
        ),
        BotCommand(
            command='start',
            description=_('START_COMMAND')
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=scope)


async def set_admin_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(
            command='cancel',
            description=_('CANCEL_COMMAND')
        ),
        BotCommand(
            command='start',
            description=_('START_COMMAND')
        ),
        BotCommand(
            command='send',
            description=_('SEND_COMMAND')
        ),
        BotCommand(
            command='stats',
            description=_('STATS_COMMAND')
        ),
    ]


    await bot.set_my_commands(commands=commands, scope=scope)
