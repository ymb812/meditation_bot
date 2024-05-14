from aiogram_dialog import DialogManager


async def get_input_data(dialog_manager: DialogManager, **kwargs):
    return {'data': dialog_manager.dialog_data}
