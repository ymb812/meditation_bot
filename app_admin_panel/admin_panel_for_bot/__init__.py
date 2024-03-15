import logging
import os
import sys
from dotenv import load_dotenv
from pydantic import ValidationError
from admin_panel_for_bot.env_models import Settings


root_logger = logging.getLogger()

if root_logger.handlers:
    root_logger.removeHandler(*root_logger.handlers)

env_paths = ['..', '']

root_logger.setLevel(logging.DEBUG)
for _p in env_paths:
    base_path = os.path.join('..', '.env')
    if os.path.exists(base_path):
        with open(os.path.join(base_path), 'r') as file:
            load_dotenv(stream=file)
        break
else:
    root_logger.setLevel(logging.INFO)


if root_logger.handlers:
    root_logger.removeHandler(*root_logger.handlers)

consoleHandler = logging.StreamHandler()

root_logger.addHandler(consoleHandler)
root_logger.setLevel(logging.INFO)
_logger = logging.getLogger(__name__)

try:
    settings = Settings(**os.environ)
except ValidationError as e:
    _logger.critical(exc_info=e, msg='Env parameters validation')
    sys.exit(-1)

if settings.debug_mode:
    _logger.info('Start in develop mode')
else:
    _logger.info('Start in production mode')