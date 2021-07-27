from flask_restful import Resource, reqparse
from flask_login import current_user

from app import create_app
from app.models import FriendRequest


class HandleFriendRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('answer',
                        type=int,
                        required=True,
                        help='missing answer'
                        ),
    parser.add_argument('friend_request',
                        type=int,
                        required=True,
                        help='missing friend request ID'
                        ),
    parser.add_argument('user',
                        type=int,
                        required=True,
                        help='missing user ID'
                        ),

    def post(self):
        print('eh')
        if not current_user.is_authenticated:
            # when sending requests without logging in
            return {'error', 'You are not logged in. Use the website to log in'}, 403
        data = HandleFriendRequest.parser.parse_args()
        print('yes')
        if data['answer'] != 0 and data['answer'] != 1:
            return {'error', 'The answer is false. Use the website to handle friend requests'}, 403
        elif data['user'] != current_user.id:
            return {'error', "Login data doesn't match. Use the website to log in and handle friend requests"}, 403
        else:

            with create_app().app_context():
                friend_request = FriendRequest.query.get(data['friend_request'])

                # accept a friend request
                if data['answer'] == 1:
                    friend_request.accept()
                    return {'success': 'friend request successfully accepted'}, 200

                # decline a friend request
                elif data['answer'] == 0:
                    friend_request.decline()
                    return {'success': 'friend request successfully declined'}, 200
