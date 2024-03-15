import re
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from core.states.registration import RegistrationStateGroup
from core.database.models import User, SupportRequest
from core.keyboards.inline import support_kb
from core.utils.texts import _


class CallBackHandler:
    __dialog_data_key = ''
    __switch_to_state = None

    @classmethod
    async def selected_content(
            cls,
            callback: CallbackQuery,
            widget: Button | Select,
            dialog_manager: DialogManager,
            item_id: str | None = None,
    ):
        # reg handlers
        if 'switch_to_phone' in callback.data:
            cls.__switch_to_state = RegistrationStateGroup.phone_input

        if item_id:
            dialog_manager.dialog_data[cls.__dialog_data_key] = item_id
        await dialog_manager.switch_to(cls.__switch_to_state)


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
        if fio.isdigit() or len(fio.split(' ')) < 2:
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
        await dialog_manager.switch_to(state=RegistrationStateGroup.confirm)


    @staticmethod
    async def entered_phone(
            message: Message,
            widget: MessageInput,
            dialog_manager: DialogManager,
    ):
        data = dialog_manager.dialog_data

        if message.contact:
            phone = message.contact.phone_number
        else:
            phone = message.text.strip()

        if not (11 <= len(phone) <= 12 and phone.replace('+', '').isdigit()):
            dialog_manager.dialog_data['error'] = 'phone_error'
            return

        await message.answer(text=_('REGISTERED'), reply_markup=ReplyKeyboardRemove())
        await message.answer(text=_('CHECK_QUESTION'), reply_markup=support_kb())

        # add reg data to DB
        await User.filter(user_id=message.from_user.id).update(
            is_registered=True,
            fio=data['fio'],
            email=data['email'],
            phone=phone,
        )

        await dialog_manager.done()


    @staticmethod
    async def entered_question(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        await SupportRequest.create(
            user_id=message.from_user.id,
            text=message.text.strip()
        )

        await message.answer(text=_('QUESTION_INFO'))
        await dialog_manager.done()
