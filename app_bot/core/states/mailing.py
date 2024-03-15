from aiogram.fsm.state import State, StatesGroup


class MailingStateGroup(StatesGroup):
    content_input = State()
