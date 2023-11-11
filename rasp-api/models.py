from passlib.hash import sha256_crypt
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from db import db_session

class Base(DeclarativeBase):
    pass

class Players(Base):
    __tablename__ = 'players'
    user_id = Column(Integer, primary_key=True) #automatically serial (auto-assigned, incremented value) with primary_key
    name = Column(String(50), nullable=False, unique=False)
    gamertag = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=func.now()) 
    last_login = Column(DateTime, onupdate=func.now())
    def check_password(self, pwd):
        return sha256_crypt.verify(pwd, self.password)