from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select
from core.dialogs.callbacks import CallBackHandler
from core.dialogs.getters import get_input_data, get_main_media_content, get_card
from core.dialogs.custom_content import CustomPager
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _


main_menu_dialog = Dialog(
    # main menu
    Window(
        DynamicMedia(selector='media_content_1'),
        Format(text='{msg_text[0]}'),
        Button(Const(text='Безоплатный сеанс Поток'), id='meditation', on_click=CallBackHandler.start_meditation),
        Button(Const(text='Счастливые числа месяца'), id='days_1', on_click=CallBackHandler.start_days),
        getter=get_main_media_content,
        state=MainMenuStateGroup.main_menu,
    ),

    # start meditation reg
    Window(
        DynamicMedia(selector='media_content_2'),
        Format(text='{msg_text[1]}'),
        Button(Const(text='ВЫБРАТЬ КАРТУ'), id='pick_cards', on_click=CallBackHandler.go_to_pick_cards),
        #SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.main_menu),
        getter=get_main_media_content,
        state=MainMenuStateGroup.start_cards,
    ),

    # pick_card
    Window(
        DynamicMedia(selector='media_content_3'),
        Format(text='{msg_text[2]}'),
        CustomPager(
            Select(
                id='_cards_select',
                items='cards',
                item_id_getter=lambda item: item.id,
                text=Format(text='Карта {item.order_priority}'),
                on_click=CallBackHandler.selected_card,
            ),
            id='card_group',
            height=6,
            width=1,
            hide_on_single_page=True,
        ),
        #SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.start_cards),
        getter=get_main_media_content,
        state=MainMenuStateGroup.pick_card
    ),

    # card
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        Button(Const(text='ХОЧУ ЕЩЕ!'), id='go_to_socials', on_click=CallBackHandler.go_to_socials),
        #SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_cards', state=MainMenuStateGroup.pick_card),
        getter=get_card,
        state=MainMenuStateGroup.card
    ),

    # socials
    Window(
        DynamicMedia(selector='media_content_4'),
        Format(text='{msg_text[3]}'),
        SwitchTo(Const(text='Вернуться к списку подарков 🎁'), id='go_to_menu', state=MainMenuStateGroup.main_menu),
        getter=get_main_media_content,
        state=MainMenuStateGroup.socials
    ),


    # start days_1
    Window(
        Format(text='{data[welcome_post_text_1]}'),
        SwitchTo(Const(text='Получить счастливые даты'), id='go_to_days_2', state=MainMenuStateGroup.days_2),
        #SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.main_menu),
        getter=get_input_data,
        state=MainMenuStateGroup.days_1,
    ),

    # day_2 - content
    Window(
        DynamicMedia(selector='media_content_5'),
        Format(text='{msg_text[4]}'),
        SwitchTo(Const(text='Вернуться к списку подарков 🎁'), id='go_to_menu', state=MainMenuStateGroup.main_menu),
        #SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.days_1),
        getter=get_main_media_content,
        state=MainMenuStateGroup.days_2,
    ),
)
