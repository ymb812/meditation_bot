import re
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
        welcome_post = await Post.get(id=settings.welcome_post_id)
        welcome_post_id_2 = await Post.get(id=settings.welcome_post_id_2)
        await bot.send_video_note(chat_id=callback.from_user.id, video_note=welcome_post.video_note_id)
        await bot.send_video_note(chat_id=callback.from_user.id, video_note=welcome_post_id_2.video_note_id)

        dialog_manager.dialog_data['welcome_post_text'] = welcome_post.text
        dialog_manager.dialog_data['reg_type'] = 'meditation'

        await dialog_manager.switch_to(MainMenuStateGroup.meditation, show_mode=ShowMode.DELETE_AND_SEND)


    @staticmethod
    async def start_days(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        dialog_manager.dialog_data['welcome_post_text_1'] = 'Вводное сообщение для дней'
        dialog_manager.dialog_data['welcome_post_text_2'] = 'В 1 месяц выдаем счастливые даты и тд бесплатно'
        dialog_manager.dialog_data['reg_type'] = 'days'

        await dialog_manager.switch_to(MainMenuStateGroup.days_1, show_mode=ShowMode.DELETE_AND_SEND)

    @staticmethod
    async def start_general_registration(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        await dialog_manager.start(state=RegistrationStateGroup.fio_input, data=dialog_manager.dialog_data)


    @staticmethod
    async def start_registration_meditation(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        await User.filter(user_id=callback.from_user.id).update(
            is_registered_meditation=True,
        )

        # send already registered msg from DB - for meditation
        registered_post = await Post.get_or_none(id=settings.registered_post_id)
        if registered_post:
            await dialog_manager.event.bot.send_message(
                chat_id=callback.from_user.id, text=registered_post.text,
            )
        else:
            await dialog_manager.event.bot.send_message(
                chat_id=callback.from_user.id, text=_('REGISTERED'),
            )

        await dialog_manager.switch_to(MainMenuStateGroup.main_menu, show_mode=ShowMode.DELETE_AND_SEND)


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
