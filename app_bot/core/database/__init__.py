from tortoise import Tortoise
from settings import settings

db_url = 'postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


async def init():
    await Tortoise.init(
        db_url=db_url.format(DB_USERNAME=settings.db_user,
                             DB_PASSWORD=settings.db_pass.get_secret_value(),
                             DB_HOST=settings.db_host,
                             DB_PORT=settings.db_port,
                             DB_NAME=settings.db_name.get_secret_value()),
        modules={'models': ['core.database.models']})
    await Tortoise.generate_schemas()


async def teardown():
    await Tortoise.close_connections()
