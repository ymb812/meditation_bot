from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.kbd import Button, SwitchTo, RequestContact
from aiogram_dialog.widgets.input import TextInput, MessageInput
from core.dialogs.getters import get_input_data
from core.dialogs.callbacks import CallBackHandler
from core.states.registration import RegistrationStateGroup
from core.utils.texts import _


registration_dialog = Dialog(
    # fio input
    Window(
        Const(text=_('FIO_INPUT')),
        TextInput(
            id='fio_input',
            type_factory=str,
            on_success=CallBackHandler.entered_fio,
        ),
        state=RegistrationStateGroup.fio_input,
    ),

    # email input
    Window(
        Const(text=_('EMAIL_INPUT')),
        TextInput(
            id='email_input',
            type_factory=str,
            on_success=CallBackHandler.entered_email
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_fio', state=RegistrationStateGroup.fio_input),
        state=RegistrationStateGroup.email_input,
    ),

    # phone input
    Window(
        Const(text=_('PHONE_INPUT')),
        RequestContact(Const(text=_('SHARE_CONTACT_BUTTON'))),
        MessageInput(func=CallBackHandler.entered_phone),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_email', state=RegistrationStateGroup.email_input),
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True),
        state=RegistrationStateGroup.phone_input,
    ),

    # confirm
    Window(
        Format(text=_('CONFIRM_INPUT_DATA',
                      fio='{data[fio]}',
                      phone='{data[phone]}',
                      email='{data[email]}',)
               ),
        Button(Const(text=_('CONFIRM_BUTTON')), id='end_of_reg', on_click=CallBackHandler.confirm_data),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_phone', state=RegistrationStateGroup.phone_input),
        getter=get_input_data,
        state=RegistrationStateGroup.confirm,
    ),
)
