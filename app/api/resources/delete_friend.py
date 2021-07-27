from flask_restful import Resource, reqparse
from flask_login import current_user

from app import create_app
from app.models import User
from app.database import db


class DoDeleteFriend(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help='missing current_user ID'
                        ),
    parser.add_argument('target_user',
                        type=int,
                        required=True,
                        help='missing target_user to unfriend'
                        )

    def post(self):
        if not current_user.is_authenticated:
            # when sending requests without logging in
            return {'error', 'You are not logged in. Use the website to log in'}, 403
        data = DoDeleteFriend.parser.parse_args()

        if data['user_id'] != current_user.id:
            return {'error', "Login data doesn't match. Use the website to log in and delete a friend"}, 403
        else:

            with create_app().app_context():
                user_to_unfriend = User.query.get(data['target_user'])
                current_user.friends.remove(user_to_unfriend)
                user_to_unfriend.friends.remove(current_user)
                db.session.commit()
