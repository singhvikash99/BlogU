#importing required modules
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#connecting to databse
engine = create_engine('mysql://root:mysql@localhost/blogu')

def db_session():
    conn = Session(engine)
    return conn