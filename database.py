from typing import Optional
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.visitors import _generate_dispatcher
from sqlalchemy_utils import EmailType



engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base()

class User(Base):

    __tablename__ = "benutzer"
    id = Column(Integer,autoincrement=True,primary_key=True)
    username= Column(String, nullable=false)
    password = Column(String, nullable=false)
    email = Column(EmailType, unique=True)
    language = Column(String)
    gender = Column(String,Optional=true)
    first_name = Column(String,Optional=true)
    last_name = Column(String,Optional=true)
    date_of_birth = Column(Date,Optional=true)


Base.metadata.create_all(engine)