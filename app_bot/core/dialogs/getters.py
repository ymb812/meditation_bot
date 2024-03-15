from aiogram_dialog import DialogManager


async def get_input_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    return {'data': data}
