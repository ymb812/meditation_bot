import re
import asyncio
import pytz
from datetime import datetime, timedelta
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.api.entities import ShowMode
from core.states.main_menu import MainMenuStateGroup
from core.states.registration import RegistrationStateGroup
from core.database.models import User, SupportRequest, Dispatcher, Post
from core.utils.texts import _
from settings import settings
from scheduler import scheduler

async def change_state_via_bg(user_dialog, user_id: int):
    # set dialog via bg if there is an active order
    if await Dispatcher.get_or_none(is_bg=True, user_id=user_id):
        await user_dialog.start(MainMenuStateGroup.socials)



class CallBackHandler:
    @staticmethod
    async def start_meditation(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        await User.filter(user_id=callback.from_user.id).update(
            is_registered_meditation=True,
        )

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

        # create order to change state in 15 minutes
        timezone = pytz.timezone('Europe/Moscow')
        send_at = datetime.now(timezone) + timedelta(minutes=15)
        if not (await Dispatcher.get_or_none(is_bg=True, user_id=callback.from_user.id)):
            await Dispatcher.create(
                post_id=1,  # useless
                is_bg=True,
                user_id=callback.from_user.id,
                send_at=send_at,
            )

        # create scheduler task, cuz we need dialog_manager.bg
        send_at = send_at - timedelta(seconds=15)
        user_dialog = dialog_manager.bg(user_id=callback.from_user.id, chat_id=callback.from_user.id)
        scheduler.add_job(change_state_via_bg, args=(user_dialog, callback.from_user.id), run_date=send_at, misfire_grace_time=10)

        dialog_manager.dialog_data['welcome_post_text'] = welcome_post_id_2.text
        dialog_manager.dialog_data['reg_type'] = 'meditation'

        await dialog_manager.switch_to(MainMenuStateGroup.start_cards, show_mode=ShowMode.DELETE_AND_SEND)


    @staticmethod
    async def go_to_pick_cards(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        # delete order and go to cards
        await Dispatcher.filter(is_bg=True, user_id=callback.from_user.id).delete()
        await dialog_manager.switch_to(state=MainMenuStateGroup.pick_card, show_mode=ShowMode.DELETE_AND_SEND)


    @staticmethod
    async def start_days(
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        await User.filter(user_id=callback.from_user.id).update(
            is_registered_days=True,
        )

        dialog_manager.dialog_data['welcome_post_text_1'] \
            = '''<b>Счастливые числа - это самые удачные дни месяца для:</b>

✨Принятия важных решений
✨Любых денежных операций (оплат, заключения сделок и тд)

Если у вас есть задача, которая никак не сдвигается с места, попробуйте приступить к ней в «счастливую» дату.

Любой сложный разговор лучше отложить до «счастливой» даты.

Зная счастливые числа месяца вы сможете спланировать важные задачи так, чтобы они прошли максимально легко и приятно для вас😘 '''

        dialog_manager.dialog_data['reg_type'] = 'days'

        await dialog_manager.switch_to(MainMenuStateGroup.days_1, show_mode=ShowMode.DELETE_AND_SEND)


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
        await dialog_manager.switch_to(MainMenuStateGroup.socials, show_mode=ShowMode.DELETE_AND_SEND)


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
