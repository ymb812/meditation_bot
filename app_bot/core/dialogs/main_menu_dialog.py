from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Start, SwitchTo
from core.dialogs.callbacks import CallBackHandler
from core.dialogs.getters import get_input_data
from core.states.main_menu import MainMenuStateGroup
from core.states.registration import RegistrationStateGroup
from core.states.support import SupportStateGroup
from core.utils.texts import _


main_menu_dialog = Dialog(
    # main menu
    Window(
        Const(text='Выберите, на что хотите зарегистрироваться'),
        Button(Const(text='Безоплатные медитации'), id='meditation', on_click=CallBackHandler.start_meditation),
        Button(Const(text='Счастливые даты '), id='days_1', on_click=CallBackHandler.start_days),
        state=MainMenuStateGroup.main_menu,
    ),

    # start meditation reg
    Window(
        Format(text='{data[welcome_post_text]}'),
        Button(Const(text=_('REGISTER_BUTTON')), id='meditation_registration', on_click=CallBackHandler.start_registration_meditation),
        Start(Const(text=_('SUPPORT_BUTTON')), id='support', state=SupportStateGroup.question_input),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.main_menu),
        getter=get_input_data,
        state=MainMenuStateGroup.meditation,
    ),

    # start days_1
    Window(
        Format(text='{data[welcome_post_text_1]}'),
        SwitchTo(Const(text='Получить счастливые даты'), id='go_to_days_2', state=MainMenuStateGroup.days_2),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.main_menu),
        getter=get_input_data,
        state=MainMenuStateGroup.days_1,
    ),

    # start days_1 reg
    Window(
        Format(text='{data[welcome_post_text_2]}'),
        Button(Const(text=_('Зарегистрироваться')), id='days_registration', on_click=CallBackHandler.start_registration_days),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.days_1),
        getter=get_input_data,
        state=MainMenuStateGroup.days_2,
    ),
)
