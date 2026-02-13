#app/models/__init__.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from helpers.config import DB_URI

Base = declarative_base()
db = Base.metadata

#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from app import app

# initialize our db
#db = SQLAlchemy(app)
#migrate = Migrate(app,db)

def create_db_connection(db_uri):
    engine = create_engine(db_uri)
    db.create_all(engine)
    
