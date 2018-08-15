from db import db
import datetime


class PollModel(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220))
    created_at = db.Column(db.String())

    choices = db.relationship('ChoiceModel', lazy='dynamic', cascade="delete")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    username = db.Column(db.String(80))
    def __init__(self, name, user_id, username):
        self.name = name
        self.user_id = user_id
        self.username = username
        self.created_at = datetime.datetime.now().__str__()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'choices': [choice.json() for choice in self.choices.all()],
            'user_id': self.user_id,
            'username': self.username,
            'created_at': self.created_at,
            'totalVotes': self.num_votes()
        }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod 
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def num_votes(self):
        k = 0
        for choice in self.choices.all():
            k+=choice.votes 
        return k

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()