import re
import logging
from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from core.states.register import RegistrationStateGroup
from core.database.models import User
from core.keyboards.inline import support_kb
from core.keyboards.reply import get_contact
from core.utils.texts import _


logger = logging.getLogger(__name__)
router = Router(name='Registration router')


@router.message(RegistrationStateGroup.fio_input)
async def fio_input(message: types.Message, state: FSMContext):
    fio = message.text.strip()

    # correct checker
    for i in fio:
        if i.isdigit():
            await message.answer(text=_('FIO_WRONG_INPUT'))
            return
    if fio.isdigit() or len(fio.split(' ')) < 2:
        await message.answer(text=_('FIO_WRONG_INPUT'))
        return

    await message.answer(text=_('EMAIL_INPUT'))

    await state.update_data(fio=fio)
    await state.set_state(RegistrationStateGroup.email_input)


@router.message(RegistrationStateGroup.email_input)
async def email_input(message: types.Message, state: FSMContext):
    email = message.text.strip()

    # correct checker
    email_regex = '^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$'
    if not re.match(email_regex, email):
        await message.answer(text=_('EMAIL_WRONG_INPUT'))
        return

    await message.answer(text=_('PHONE_INPUT'), reply_markup=get_contact())

    await state.update_data(email=email)
    await state.set_state(RegistrationStateGroup.phone_input)


@router.message(RegistrationStateGroup.phone_input)
async def phone_input(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text.strip()

    if not (11 <= len(phone) <= 12 and phone.replace('+', '').isdigit()):
        await message.answer(text=_('PHONE_WRONG_INPUT'))
        return

    await message.answer(text=_('REGISTERED'), reply_markup=ReplyKeyboardRemove())
    await message.answer(text=_('CHECK_QUESTION'), reply_markup=support_kb())

    # add reg data to DB
    state_data = await state.get_data()
    await User.filter(user_id=message.from_user.id).update(
        is_registered=True,
        fio=state_data['fio'],
        email=state_data['email'],
        phone=phone,
    )

    await state.clear()



