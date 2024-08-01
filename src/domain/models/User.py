from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import BaseUser

class User(BaseUser):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String, nullable=True)
    name = Column(String, nullable=False)
    cellphone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, nullable=True)

