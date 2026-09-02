import logging

if __name__ == 'app.models':
    BASE_MODELS = ['app','models']
    from app.helpers.common import whoami
    from app.helpers.constants import APPLICATION_NAME
else:
    BASE_MODELS = ['models']
    from helpers.common import whoami
    from helpers.constants import APPLICATION_NAME

mod_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{mod_name}')
mod_logger.debug('Entering module %s',mod_name)

import os
from pathlib import Path
from importlib import import_module

try:
    for m in os.listdir(Path(__file__).parent.resolve()):
        if m.endswith('.py') and m != '__init__.py':
            model = '.'.join(BASE_MODELS+m.split('.')[:-1])
            mod_logger.info('Importing database model - %s', model)
            import_module(model)
except Exception as e:
    raise e
finally:
    mod_logger.debug('Leaving module %s',mod_name)
