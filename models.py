from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DATETIME
from flask_login import UserMixin





#Base class
class Base (DeclarativeBase):
    pass

#class for coloums in database
class Users(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    First_name: Mapped[str] = mapped_column (String (50))
    Last_name: Mapped[str] = mapped_column (String(50))
    Email: Mapped[str] = mapped_column (String(50))
    Username = mapped_column (String(50))
    Ph_no: Mapped[str] = mapped_column (String(10))
    Pass: Mapped[str] = mapped_column (String(100))
    Created_at: Mapped[str] = mapped_column (DATETIME)
    Updated_at: Mapped[str] = mapped_column (DATETIME)


    # def get_id(self):
    #     return str(self.Id)


