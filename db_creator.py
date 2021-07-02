# -*- coding: utf-8> -*-
from database import User, Data
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User,Data
engine = create_engine('sqlite:///app.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()

salt = (b"100000")
key = hashlib.pbkdf2_hmac(
    'sha256',  # The hash digest algorithm for HMAC
    "   ".encode("UTF-8"),  # Convert the password to bytes
    salt,  # Provide the salt
    100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    dklen=128  # Get a 128 byte key
)



#new_user=User(username="sa6o", password=key, email="sa6o@sa6o.com", language="de")
#db_session.add(new_user)
#db_session.commit()
#print(user_id)
db_session.add(Data(user_id = 1))
db_session.commit()
#db_session.commit()
#print(db_session.query(User).filter_by(id = user_id).first())
#print(db_session.query(Data).filter_by(user_id = user_id).first())
#db_session.query(Data).filter_by(user_id = user_id).update({'first_name': "sa60"})
print(db_session.query(Data).filter_by(id = 1).first())
#db_session.query(Data).filter_by(user_id = 1).update({'gender': "Male"})
db_session.commit()