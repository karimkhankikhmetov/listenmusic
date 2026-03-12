from sqlalchemy import Column, String, Integer
from app.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    original_name = Column(String)
    stored_name = Column(String)
    author = Column(String)
    duration = Column(Integer)
    file_size = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)