from app import db


class Comment(db.Model):
    """
    contains comments submitted by users on individual posts
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    text = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, time, text, user_id=None, post_id=None):
        self.time = time
        self.text = text
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return f'Comment ID: {self.id}'

    @classmethod
    def add(cls, time, text, user_id, post_id):
        comment = cls(time, text, user_id, post_id)
        db.session.add(comment)
        db.session.commit()
