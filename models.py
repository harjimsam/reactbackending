import datetime
from sqlalchemy.orm import relationship

from init import db,app


class User(db.Model):
    __tablename__ = 'rusers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    '''
    questions = relationship("Question",
                         order_by="desc(Question.date)",
                         primaryjoin="Question.creator_id==User.id")
    '''

    def __init__(self,username, password):
        self.username = username
        self.password = password

#create
db.create_all(app=app)
