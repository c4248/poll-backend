from models.ChoiceVote import ChoiceVote
from flask_restful import Resource

class ChoiceVoteList(Resource):
    def get(self):
        return {'choice_votes': [choicevote.json() for choicevote in ChoiceVote.find_all()]}