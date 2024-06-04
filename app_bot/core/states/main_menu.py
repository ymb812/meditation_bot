from aiogram.fsm.state import State, StatesGroup


class MainMenuStateGroup(StatesGroup):
    main_menu = State()

    start_cards = State()
    pick_card = State()
    card = State()
    socials = State()

    days_1 = State()
    days_2 = State()
