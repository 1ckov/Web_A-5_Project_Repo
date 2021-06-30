from app import db
from app import User

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User,Data
engine = create_engine('sqlite:///app.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()
print(User.query.all())

db.session.add(User(username="momo", password="   ", email="ads.sd", language="en"))

print(User.query.all())

db.session.commit()