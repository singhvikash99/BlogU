from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DATETIME





#Base class
class Base (DeclarativeBase):
    pass

#class for coloums in database
class Users(Base):
    __tablename__ = "users"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    First_name: Mapped[str] = mapped_column (String (50))
    Last_name: Mapped[str] = mapped_column (String(50))
    Email: Mapped[str] = mapped_column (String(50))
    Ph_no: Mapped[str] = mapped_column (String(10))
    Pass: Mapped[str] = mapped_column (String(50))
    Created_at: Mapped[str] = mapped_column (DATETIME)
    Updated_at: Mapped[str] = mapped_column (DATETIME)
    Username: Mapped[str] = mapped_column (String(50))


