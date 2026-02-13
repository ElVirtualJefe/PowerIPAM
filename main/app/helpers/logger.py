"""
Docstring for main.app.helpers.logger
"""

import logging
from pathlib import Path
from helpers.constants import DEFAULT_LOG_FORMAT,DEFAULT_LOG_DIR

class Logger():

    def __repr__(self):
        print(f"""<
              Logger {__name__}
              >""")

def setup_basic_logging(level=logging.DEBUG,fmt=DEFAULT_LOG_FORMAT,dir=DEFAULT_LOG_DIR) -> None:
    """
    Docstring for setup_basic_logging
    
    :param level: Description
    :param format: Description
    """

    if not Path.is_dir(dir):
        Path(dir).mkdir(644,parents=True)

    logging.basicConfig(level=level,
                        format=fmt,
                        filename=f'{dir}/PowerIPAM-debug.log')
    
    return

