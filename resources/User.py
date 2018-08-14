from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)
from models.User import UserModel 
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import datetime

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
_user_parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

_if_user_parser = reqparse.RequestParser()
_if_user_parser.add_argument('username', type=str, required=True)

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        
        elif len(data['username'])<4:
            return {"message": "Username must have more than 3 characters"}, 400
        
        elif len(data['password'])<8:
            return {"message": "Password must have more than 7 characters"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201 

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404 
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200 
    
    @classmethod
    def post(cls, user_id):
        data = _if_user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user:
            return {'isRegistered': True}
        return {'isRegistered': False}

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            expires = datetime.timedelta(minutes=30)
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_id': user.id
            }, 200

        return {'message': 'Invalid credentials'}, 401 

class UserLogout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
