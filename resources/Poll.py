from flask_restful import Resource, reqparse, request 
from models.Poll import PollModel
from models.Choice import ChoiceModel
from models.User import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from random import randint

class Poll(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('choice_list', action='append')
    parser.add_argument('name', type=str)
    parser.add_argument('admin', type=bool)
    def get(self, id):
        poll = PollModel.find_by_id(id)
        if poll:
            return poll.json()
        return {'message': 'poll not found'}, 404

    @jwt_required
    def post(self):
        data = Poll.parser.parse_args()
        user = UserModel.find_by_id(get_jwt_identity())
        poll = PollModel(data.name, user.id, user.username)
        try: 
            poll.save_to_db()
            for choice in data.choice_list:
                if data.admin:
                    choice_to_save = ChoiceModel(choice, randint(80,1000), poll.id)
                else:
                choice_to_save = ChoiceModel(choice, 0, poll.id)
                choice_to_save.save_to_db()
        except:
            return {'message': 'Server error'}, 500
        return poll.json(), 201

    def delete(self, id):
        poll = PollModel.find_by_id(id)
        if poll:
            poll.delete_from_db()
            return {'message': 'poll deleted'}
        return {'message': 'cannot find poll with given id'}


class PollList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        polls = PollModel.query.order_by(PollModel.id.desc()).paginate(page, 10, False)
        polls_json = [poll.json() for poll in polls.items]
        return {
            'polls': polls_json,
            'hasNext': polls.has_next
        }