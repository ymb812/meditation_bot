import datetime
import logging
from aiogram import Bot, types, Router, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram_dialog import DialogManager, StartMode
from core.states.registration import RegistrationStateGroup
from core.states.support import SupportStateGroup
from core.utils.texts import set_user_commands, set_admin_commands, _
from core.database.models import User, Post, Dispatcher
from core.keyboards.inline import menu_kb, support_kb
from settings import settings


logger = logging.getLogger(__name__)
router = Router(name='Start router')


@router.message(Command(commands=['start']), StateFilter(None))
async def start_handler(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()

    # check channel for user
    chat_member = await bot.get_chat_member(user_id=message.from_user.id, chat_id=settings.required_channel_id)
    if chat_member.status not in ['creator', 'administrator', 'member', 'restricted']:
        logger.info(f'user_id={message.from_user.id} is not in the chat')
        channel_link = await bot.create_chat_invite_link(chat_id=settings.required_channel_id)
        await message.answer(
            text=_('NOT_FOLLOWED', channel_link=channel_link.invite_link)
        )
        return

    # add basic info to db
    await User.update_data(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_premium=message.from_user.is_premium,
    )

    user = await User.get(user_id=message.from_user.id)
    if user.is_registered:
        await message.answer(text=_('ALREADY_REGISTERED'), reply_markup=support_kb())
        return

    if user.status == 'admin':
        await set_admin_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
    else:
        await set_user_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))

    # create order for notification if there is no
    if not (await Dispatcher.get_or_none(post_id=settings.notification_post_id, user_id=message.from_user.id)):
        await Dispatcher.create(
            post_id=settings.notification_post_id,
            user_id=message.from_user.id,
            send_at=datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        )

    # send welcome msg from DB
    welcome_post = await Post.get(id=settings.welcome_post_id)
    await message.answer_video_note(video_note=welcome_post.video_note_id)
    await message.answer(text=welcome_post.text, reply_markup=menu_kb())


# register support
@router.callback_query(lambda c: c.data in ['register', 'support'])
async def menu_handler(callback: types.CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
    # going to the register or support FSM
    if callback.data == 'register':
        await dialog_manager.start(state=RegistrationStateGroup.fio_input, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(state=SupportStateGroup.question_input, mode=StartMode.RESET_STACK)
