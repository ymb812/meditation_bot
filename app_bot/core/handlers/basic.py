import logging
import asyncio
from aiogram import types, Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from settings import settings
from core.database.models import User
from core.utils.texts import set_admin_commands, _

logger = logging.getLogger(__name__)
router = Router(name='Basic commands router')


# ez to get id while developing
@router.channel_post(Command(commands=['init']))
@router.message(Command(commands=['init']))
async def init_for_id(message: types.Message):
    await message.delete()
    msg = await message.answer(text=f'<code>{message.chat.id}</code>')
    await asyncio.sleep(2)
    await msg.delete()


# admin login
@router.message(Command(commands=['admin']))
async def admin_login(message: types.Message, state: FSMContext, command: CommandObject, bot: Bot):
    if command.args == settings.admin_password.get_secret_value():
        await state.clear()
        await message.answer(text=_('NEW_ADMIN_TEXT'))
        await User.set_status(user_id=message.from_user.id, status='admin')
        await set_admin_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
