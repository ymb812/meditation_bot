from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.callbacks import CallBackHandler
from core.states.support import SupportStateGroup
from core.utils.texts import _


support_dialog = Dialog(
    # question input
    Window(
        Const(text=_('QUESTION_INPUT')),
        TextInput(
            id='question_input',
            type_factory=str,
            on_success=CallBackHandler.entered_question,
        ),
        state=SupportStateGroup.question_input,
    ),
)
