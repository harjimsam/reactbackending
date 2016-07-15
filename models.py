import datetime
from sqlalchemy.orm import relationship

from init import db,app


class User(db.Model):
    __tablename__ = 'husers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(61))


    def __init__(self,username, password):
        self.username = username
        self.password = password

#create
db.create_all(app=app)
