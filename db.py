#importing required modules
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import String, Integer, DATETIME, create_engine, select
from datetime import datetime

#connecting to databse
engine = create_engine('mysql://root:mysql@localhost/blogu')

#Base class
class Base (DeclarativeBase):
    pass

#class for coloums in database
class Users(Base):
    __tablename__ = "users"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    First_name: Mapped[str] = mapped_column (String (50))
    Last_name: Mapped[str] = mapped_column (String(50))
    Email: Mapped[str] = mapped_column (String(50))
    Ph_no: Mapped[str] = mapped_column (String(10))
    Pass: Mapped[str] = mapped_column (String(50))
    Created_at: Mapped[str] = mapped_column (DATETIME)
    Updated_at: Mapped[str] = mapped_column (DATETIME)
    Username: Mapped[str] = mapped_column (String(50))

#initiating session
conn = Session(engine)

#adding data 
""" new_user = Users()
new_user.ID = 5
new_user.First_name = "Raju"
new_user.Last_name = "Verma"
new_user.Email = "rajuverma@gmail.com"
new_user.Ph_no = "9677876676"
new_user.Pass = "asbwucbabwa"
new_user.Created_at = datetime.now()
new_user.Updated_at = datetime.now()
new_user.Username = "iamraju"

conn.add(new_user)
conn.commit() """


#fetching data
res = conn.scalars(select(Users)).all()
for i in res:
    print (i.First_name, i.Username, i.Pass)


#closing session
conn.close()



