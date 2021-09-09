from datetime import datetime
from adv import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    "function returns user id of user that is logged in"
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    A class to represent and save a User in the database.

    ...

    Attributes
    ----------
    id: db.Column
        unique id each user in database must have
    username : db.Column
        username of the user
    email : db.Column
        email of the user
    date_created: db.Column
        date the user's account was created
    password: db.Column
        password of the user
    graphs_created: db.Column
        number of graphs created by the user
    videos: db.relationship
        videos saved by the user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    graphs_created =  db.Column(db.Integer, default = 0)
    videos = db.relationship('Video', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Video(db.Model):
    """
    A class to represent and save a User in the database.

    ...

    Attributes
    ----------
    id: db.Column
        unique id each video in database has
    htmlcode : db.Column
        htmlcode of each video
    user_id : db.Column
        which user created this video
    """
    id = db.Column(db.Integer, primary_key=True)
    htmlcode = db.Column(db.String(1000000000000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.id}')"

if __name__ == '__main__':
    db.create_all()