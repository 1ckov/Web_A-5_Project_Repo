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

    __tablename__ = "user"
    id = Column(Integer,autoincrement=True,primary_key=True)
    username= Column(String, nullable=false)
    password = Column(String, nullable=false)
    email = Column(EmailType, unique=True)
    language = Column(String)
    gender = Column(String,nullable=true)
    first_name = Column(String,nullable=true)
    last_name = Column(String,nullable=true)
    date_of_birth = Column(Date,nullable=true)
    data = relationship("Data", back_populates="user", uselist= False)
    
    def __repr__(self):
       return "User: "+ str(self.username) + " /Id: "+ str(self.id) +" /Pass: "+ str(self.password)+ " /Email: " + str(self.email) + " /Language: " + str(self.language)


class Data(Base):

    __tablename__ = "data"
    id = Column(Integer ,primary_key=true)
    user_id = Column(Integer, ForeignKey('user.id'),unique=true)  
    user = relationship("User", back_populates="data")                                                 
    gender = Column(Boolean,nullable=true)
    first_name = Column(String,nullable=true)
    last_name = Column(String,nullable=true)
    date_of_birth = Column(Date,nullable=true)
    registration_date = Column(Date,nullable=true)              ##Anmeldedatum
    street = Column(String,nullable=true)                       ##Stra&#223;e
    streetnumber = Column(String,nullable=true)
    address_addition = Column(String,nullable=true)             ##Adresszusatz
    zip_code = Column(Integer,nullable=true)
    city = Column(String,nullable=true)
    phone_number = Column(String,nullable=true)
    timespan = Column(String,nullable=true)                     #1 = 45 days
                                                                #2 = 3 Months before
                                                                #3 = 6 Months before
                                                                #4 = 12 Months before
    type_of_transfer = Column(Boolean,nullable=true)            ##true = sepa## 
    name_sepa = Column(String,nullable=true)
    street_sepa = Column(String,nullable=true)                  ##Stra&#223;e_Lastschrift
    streetnumber_sepa = Column(String,nullable=true)            ##HausnummerLastschrift
    zip_code_sepa = Column(String,nullable=true)                ##PLZLastschrift
    city_sepa = Column(String,nullable=true)                    ##OrtLastschrift
    IBAN = Column(String,nullable=true)
    BIC = Column(String,nullable=true)

    credit_institution = Column(String,nullable=true)



Base.metadata.create_all(engine)