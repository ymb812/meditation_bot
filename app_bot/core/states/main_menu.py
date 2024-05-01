from aiogram.fsm.state import State, StatesGroup


class MainMenuStateGroup(StatesGroup):
    main_menu = State()
    meditation = State()
    days_1 = State()
    days_2 = State()
