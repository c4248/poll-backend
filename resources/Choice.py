from flask_restful import Resource, reqparse 
from models.Choice import ChoiceModel
from models.ChoiceVote import ChoiceVote
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.User import UserModel

class Choice(Resource):
    
    def get(self, id):
        choice = ChoiceModel.find_by_id(id)
        if choice:
            return choice.json()
        return {'message': 'choice is not found'}, 404

    @jwt_required
    def post(self, id):
        choice = ChoiceModel.find_by_id(id)
        if choice:
            user = UserModel.find_by_id(get_jwt_identity())
            choiceVote = ChoiceVote(
                choice.choice,
                choice.poll_id, 
                choice.id,
                user.username,
                user.id
                
            )
            choiceVote.save_to_db()
            choice.votes += 1
            choice.save_to_db()
        return choice.json()
