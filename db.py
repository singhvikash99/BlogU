from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models import Base

engine = create_engine('sqlite:///blogu.db')

def db_session():
    try:
        Base.metadata.create_all(engine)
        conn = Session(engine)
        return conn
    
    except Exception as err:
        return {"details": str(err)}
