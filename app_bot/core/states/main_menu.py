from aiogram.fsm.state import State, StatesGroup


class MainMenuStateGroup(StatesGroup):
    general_registration = State()
    main_menu = State()
    meditation = State()
    days_1 = State()
    days_2 = State()
