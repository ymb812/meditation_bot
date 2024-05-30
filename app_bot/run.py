import asyncio
import logging
import core.middlewares
from aiogram import Bot, Dispatcher, filters
from aiogram_dialog import setup_dialogs, DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from settings import settings
from setup import register
from core.handlers import routers
from core.dialogs import dialogues
from core.states.main_menu import MainMenuStateGroup
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from scheduler import scheduler

logger = logging.getLogger(__name__)


async def handle_unknown_intent_or_state(event, dialog_manager: DialogManager):
    logger.error('Restarting dialog: %s', event.exception)
    await dialog_manager.start(
        MainMenuStateGroup.main_menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND,
    )

bot = Bot(settings.bot_token.get_secret_value(), parse_mode='HTML')

storage = RedisStorage.from_url(
    url=f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_name}',
    key_builder=DefaultKeyBuilder(with_destiny=True)
)
dp = Dispatcher(storage=storage)
core.middlewares.i18n.setup(dp)
setup_dialogs(dp)

# handle errors for old dialog
dp.errors.register(
    handle_unknown_intent_or_state,
    filters.ExceptionTypeFilter(UnknownIntent, UnknownState),
)

for _r in routers + dialogues:
    dp.include_router(_r)

async def main():
    async with register():
        scheduler.start()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
