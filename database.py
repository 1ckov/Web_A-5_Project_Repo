from typing import Optional
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.visitors import _generate_dispatcher
from sqlalchemy_utils import EmailType, PhoneNumber



engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base()

class User(Base):

    __tablename__ = "benutzer"
    User_id = Column(Integer,autoincrement=True,primary_key=True)
    username= Column(String, nullable=false)
    password = Column(String, nullable=false)
    email = Column(EmailType, unique=True)
    language = Column(String)
    gender = Column(String,nullable=true)
    first_name = Column(String,nullable=true)
    last_name = Column(String,nullable=true)
    date_of_birth = Column(Date,nullable=true)
    daten = relationship("daten", backref='benutzer', uselist=false)


class Daten(Base):

    __tablename__ = "daten"
    id = Column(Integer ,primary_key=true)
    User_id = Column(Integer, ForeignKey('benutzer'),unique=true)                                                   
    gender = Column(String,nullable=true)
    first_name = Column(String,nullable=true)
    last_name = Column(String,nullable=true)
    date_of_birth = Column(Date,nullable=true)
    street = Column(String,nullable=true)
    streetnumber = Column(String,nullable=true)
    address_addition = Column(String,nullable=true)
    zip_code = Column(Integer,nullable=true)
    city = Column(String,nullable=true)
    phone_number = Column(String,nullable=true)
    timespan = Column(String,nullable=true)
    type_of_transfer = Column(Boolean,nullable=true)            ##true = sepa## 
    name = Column(String,nullable=true)
    IBAN = Column(String,nullable=true)
    BIC = Column(String,nullable=true)
    credit_institution = Column(String,nullable=true)

Base.metadata.create_all(engine)