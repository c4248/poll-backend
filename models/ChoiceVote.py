from db import db

class ChoiceVote(db.Model):
    __tablename__ = 'choicevote'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    choice = db.Column(db.String(80))
    choice_id = db.Column(db.Integer)
    username = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, choice, question_id, choice_id, username, user_id):
        self.choice = choice
        self.choice_id = choice_id
        self.question_id = question_id
        self.username = username
        self.user_id = user_id
    
    def json(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'choice': self.choice,
            'choice_id': self.choice_id,
            'username': self.username,
            'user_id': self.user_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()