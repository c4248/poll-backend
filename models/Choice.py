from db import db

class ChoiceModel(db.Model):
    __tablename__ = 'choice'

    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(220))
    votes = db.Column(db.Integer)

    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))
    poll = db.relationship('PollModel')

    def __init__(self, choice, votes, poll_id):
        self.choice = choice
        self.votes = votes
        self.poll_id = poll_id

    def json(self):
        return {
            'poll_id': self.poll_id,
            'choice': self.choice,
            'votes': self.votes,
            'id': self.id
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()