from aiogram.fsm.state import State, StatesGroup


class SupportStateGroup(StatesGroup):
    question_input = State()
