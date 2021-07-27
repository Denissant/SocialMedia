from flask_restful import Api
from .resources.friend_requests import HandleFriendRequest

api = Api(prefix='/api/')


api.add_resource(HandleFriendRequest, '/friend')
