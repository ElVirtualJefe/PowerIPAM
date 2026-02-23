#app/models/__init__.py
from logging import getLogger,currentframe
from helpers.common import whoami
from helpers.constants import APPLICATION_NAME

mod_name = whoami(currentframe())
#print(f'{mod_name=}')
mod_logger = getLogger(f'{APPLICATION_NAME}.{mod_name}')
mod_logger.debug('Entering module %s', mod_name)


#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from app import app

# initialize our db
#db = SQLAlchemy(app)
#migrate = Migrate(app,db)

def create_db_connection(db_uri):
    """
    Docstring for create_db_connection
    
    :param db_uri: Description
    """
    func_name = whoami(currentframe())
    mod_logger.debug('Entering function %s', func_name)

    try:
        from sqlalchemy.orm import sessionmaker,scoped_session                                                                    
        from sqlalchemy import create_engine
        from helpers.config import DB_NAME
        from helpers.constants import BASE
        import models

        engine = create_engine(db_uri)
        mod_logger.debug(f'{engine.url=}')

        SESSION = scoped_session(sessionmaker(bind=engine))
        mod_logger.info('Successfully created DB Connection...')

        db = BASE.metadata
        db.create_all(engine)
        mod_logger.debug('Created all tables in %s', DB_NAME)

        return SESSION()

    except Exception as e:
        mod_logger.critical('Critical Error setting up database connection.')
        raise  e
    finally:
        mod_logger.debug('Leaving function %s', func_name)


    
mod_logger.debug('Leaving module %s', mod_name)
