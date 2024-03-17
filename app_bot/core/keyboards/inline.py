from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.texts import _


def mailing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('MAILING_BUTTON'), callback_data='start_mailing')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('REGISTER_BUTTON'), callback_data='register')
    kb.button(text=_('SUPPORT_BUTTON'), callback_data='support')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def support_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('SUPPORT_BUTTON'), callback_data='support')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def followed_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('FOLLOWED_BUTTON'), callback_data='followed')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
