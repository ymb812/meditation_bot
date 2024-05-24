import re
import asyncio
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.api.entities import ShowMode
from core.states.main_menu import MainMenuStateGroup
from core.states.registration import RegistrationStateGroup
from core.database.models import User, SupportRequest, Dispatcher, Post
from core.keyboards.inline import support_kb
from core.utils.texts import _
from settings import settings


class CallBackHandler:
    @staticmethod
    async def start_meditation(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        # send 2 welcome msgs from DB
        bot = dialog_manager.event.bot
        welcome_post_id_2 = await Post.get(id=settings.welcome_post_id_2)

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=welcome_post_id_2.text,
        )
        await bot.send_chat_action(chat_id=callback.from_user.id, action='record_video_note')
        await asyncio.sleep(0.5)
        await bot.send_video_note(chat_id=callback.from_user.id, video_note=welcome_post_id_2.video_note_id)

        # TODO: CREATE ORDER FOR BG TO CHANGE STATE IN 15 MINUTES  !!!

        dialog_manager.dialog_data['welcome_post_text'] = welcome_post_id_2.text
        dialog_manager.dialog_data['reg_type'] = 'meditation'
        dialog_manager.dialog_data['main_menu_post_id'] = 1007

        await dialog_manager.switch_to(MainMenuStateGroup.start_cards, show_mode=ShowMode.DELETE_AND_SEND)


    @staticmethod
    async def start_days(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        dialog_manager.dialog_data['welcome_post_text_1'] \
            = '''Счастливые числа - это наиболее удачные дни месяца для:
✨Принятия важных решений
✨Любых итераций с деньгами (оплат, заключения сделок и тд)

Если у вас есть задача, которая никак не сдвигается с места, попробуйте приступить к ней в «счастливую» дату.

Любой сложный разговор лучше отложить до «счастливой» даты.

Зная счастливые числа месяца вы сможете спланировать важные задачи так, чтобы они прошли максимально легко и приятно для вас 😘'''

        dialog_manager.dialog_data['reg_type'] = 'days'

        await dialog_manager.switch_to(MainMenuStateGroup.days_1, show_mode=ShowMode.DELETE_AND_SEND)

    # TODO: USELESS
    @staticmethod
    async def start_general_registration(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        await dialog_manager.start(state=RegistrationStateGroup.fio_input, data=dialog_manager.dialog_data)


    @staticmethod
    async def selected_card(
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        dialog_manager.dialog_data['card_id'] = item_id
        await dialog_manager.switch_to(MainMenuStateGroup.card)


    @staticmethod
    async def go_to_socials(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        # send voice
        voice = await Post.get(id=1011)
        await dialog_manager.event.bot.send_voice(
            chat_id=callback.from_user.id,
            voice=voice.sticker_file_id,
            caption=voice.text,
        )

        await dialog_manager.switch_to(MainMenuStateGroup.socials, show_mode=ShowMode.DELETE_AND_SEND)


    # TODO: USELESS
    @staticmethod
    async def start_registration_days(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        await User.filter(user_id=callback.from_user.id).update(
            is_registered_days=True,
        )

        # send already registered msg from DB - for days
        days_post = await Post.get_or_none(id=settings.days_post_id)
        await callback.message.answer_photo(photo=days_post.photo_file_id, caption=days_post.text)
        await dialog_manager.switch_to(MainMenuStateGroup.main_menu, show_mode=ShowMode.DELETE_AND_SEND)


    @staticmethod
    async def entered_fio(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        # correct checker
        fio = message.text.strip()
        for i in fio:
            if i.isdigit():
                return
        if fio.isdigit() or len(fio.split(' ')) > 5:
            return

        value: str
        dialog_manager.dialog_data['fio'] = value
        await dialog_manager.switch_to(state=RegistrationStateGroup.email_input)


    @staticmethod
    async def entered_email(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        # correct checker
        email = message.text.strip()
        email_regex = '^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$'
        if not re.match(email_regex, email):
            return

        value: str
        dialog_manager.dialog_data['email'] = value
        await dialog_manager.switch_to(state=RegistrationStateGroup.phone_input)


    @staticmethod
    async def entered_phone(
            message: Message,
            widget: MessageInput,
            dialog_manager: DialogManager,
    ):
        if message.contact:
            phone = message.contact.phone_number
        else:
            phone = message.text.strip()

        dialog_manager.dialog_data['phone'] = phone
        await dialog_manager.switch_to(state=RegistrationStateGroup.confirm)


    @staticmethod
    async def confirm_data(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        user = await User.get(user_id=callback.from_user.id)

        user.is_registered = True
        user.fio = dialog_manager.dialog_data['fio']
        user.phone = dialog_manager.dialog_data['phone']
        user.email = dialog_manager.dialog_data['email']
        await user.save()

        # delete notification order
        await Dispatcher.filter(post_id=settings.notification_post_id, user_id=callback.from_user.id).delete()

        await dialog_manager.start(state=MainMenuStateGroup.main_menu, show_mode=ShowMode.DELETE_AND_SEND)


    @staticmethod
    async def entered_question(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        question = message.text.strip()
        await SupportRequest.create(
            user_id=message.from_user.id,
            text=question,
        )

        # send question to admin
        if message.from_user.username:
            username = f'@{message.from_user.username}'
        else:
            username = f'<a href="tg://user?id={message.from_user.id}">ссылка</a>'
        await dialog_manager.middleware_data['bot'].send_message(
            chat_id=settings.admin_chat_id, text=_('QUESTION_FROM_USER', username=username, question=question)
        )

        await message.answer(text=_('QUESTION_INFO'))
        await dialog_manager.done()
