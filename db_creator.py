
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User,Data
from passlib.hash import sha256_crypt
engine = create_engine('sqlite:///app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


session.add(User(username="sa6o", password=sha256_crypt("   "), email="sdadwqe.sd", language="en"))
print(session.query(User))

session.commit()