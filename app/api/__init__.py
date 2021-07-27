from flask_restful import Api
from .resources.friend_requests import HandleFriendRequest
from .resources.delete_friend import DoDeleteFriend

api = Api(prefix='/api/')


api.add_resource(HandleFriendRequest, '/friendrequest')
api.add_resource(DoDeleteFriend, '/deletefriend')

