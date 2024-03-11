from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DATETIME, Text, ForeignKey
from flask_login import UserMixin
from typing import List


"""
for response_type
Like = 1
Comment = 2
"""

#Base class
class Base (DeclarativeBase):
    pass

#class for users table in database
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

    user_blogs: Mapped[List["Blogs"]] = relationship(back_populates= "blogs_user")
    users_responses: Mapped[List['Response']] = relationship(back_populates="responses_users")

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    category: Mapped[str] = mapped_column (String(45))

    category_blogs: Mapped[List["Blogs"]] = relationship(back_populates="blogs_category")

#class for blogs table in database
class Blogs(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[str] = mapped_column (ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column (ForeignKey("category.id"))
    content: Mapped[str] = mapped_column (Text)
    title: Mapped[str] = mapped_column (String(128))
    is_deleted: Mapped[int] = mapped_column (Integer)
    created_at: Mapped[str] = mapped_column (DATETIME)
    updated_at: Mapped[str] = mapped_column (DATETIME)

    blogs_user: Mapped["Users"] = relationship(back_populates="user_blogs")
    blogs_category: Mapped["Category"] = relationship(back_populates="category_blogs")
    blogs_responses: Mapped[List['Response']] = relationship(back_populates="responses_blogs")

class Response(Base):
    __tablename__ = "response"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    blog_id: Mapped[int] = mapped_column(ForeignKey('blogs.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    response_type: Mapped[int] = mapped_column(Integer)
    response_arg: Mapped[str] = mapped_column(String(128))

    responses_users: Mapped['Users'] = relationship(back_populates="users_responses")
    responses_blogs: Mapped['Blogs'] = relationship(back_populates="blogs_responses")

