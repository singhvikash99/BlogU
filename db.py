#importing required modules
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#connecting to databse
engine = create_engine('mysql://root:mysql@localhost/blogu')

def db_session():
    try:
        conn = Session(engine)
        print ("connected")
        return conn
    
    except Exception as err:
        return {"details": str(err)}