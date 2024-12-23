from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime

from internal.repository.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
