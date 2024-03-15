from aiogram.fsm.state import State, StatesGroup


class RegistrationStateGroup(StatesGroup):
    fio_input = State()
    email_input = State()
    phone_input = State()
