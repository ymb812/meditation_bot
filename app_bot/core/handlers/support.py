import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from core.states.support import SupportStateGroup
from core.utils.texts import _
from core.database.models import SupportRequest


logger = logging.getLogger(__name__)
router = Router(name='Support router')


@router.message(SupportStateGroup.question_input)
async def support_handler(message: types.Message, state: FSMContext):
    await SupportRequest.create(
        user_id=message.from_user.id,
        text=message.text.strip()
    )

    await message.answer(text=_('QUESTION_INFO'))
    await state.clear()
