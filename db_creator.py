from app import db
from app import User

print(User.query.all())

db.session.add(User(username="momo", password="   ", email="ads.sd", language="en"))

print(User.query.all())

db.session.commit()