import os
import jwt
import datetime
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

follows = db.Table('follows',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
                   )

likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                 )

comment_likes = db.Table('comment_likes',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'))
                         )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.String(100))
    following = db.relationship(
        'User', secondary=follows,
        primaryjoin=(follows.c.user_id == id),
        secondaryjoin=(follows.c.following_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    posts = db.relationship('Post', backref='author')
    replies = db.relationship('Comment', backref='author')

    def __repr__(self):
        return 'User: ' + self.username

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def user_to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'followers': self.followers.count(),
            'following': self.following.count()
        }

    def is_following(self, user):
        return self.following.filter(
            follows.c.following_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def has_liked_post(self, post):
        return self.liked_posts.filter(
            likes.c.post_id == post.id).count() > 0

    def like_post(self, post):
        if not self.has_liked_post(post):
            self.liked_posts.append(post)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            self.liked_posts.remove(post)

    def has_liked_comment(self, comment):
        return self.liked_comments.filter(
            comment_likes.c.comment_id == comment.id).count() > 0

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            self.liked_comments.append(comment)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            self.liked_comments.remove(comment)

    def generate_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                'secret_key',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token Expired'
        except jwt.InvalidTokenError:
            return "Invalid Token."


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship('User', secondary='likes', backref=db.backref('liked_posts', lazy='dynamic'),
                            lazy='dynamic')
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return '<Content : {}>'.format(self.body)

    def get_comments(self):
        comments_array = []
        for comment in self.comments:
            comments_array.append(comment.comment_to_json())
        return comments_array[::-1]

    def post_to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'author': self.author.user_to_json(),
            'no_of_likes': self.likes.count(),
            'no_of_comments': len(self.comments),
            'comments': self.get_comments()
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    replies = db.Column(db.String, default='')
    likes = db.relationship('User', secondary='comment_likes', backref=db.backref('liked_comments', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return '<Comment : {}, Post : {}>'.format(self.body, self.post_id)

    def comment_to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'no_of_likes': self.likes.count(),
            'author': self.author.user_to_json(),
            'post_id': self.post_id,
            'replies': len(self.get_replies())
        }

    def rtype(self):
        return type(self.replies)

    def add_reply(self, body, author):
        c = Comment(body=body, post=self.post, author=author)
        db.session.add(c)
        db.session.commit()
        self.replies += str(c.id) + ','
        db.session.commit()
        return c

    def get_replies(self):
        replies = self.replies.replace(",", "")
        replies_arr = []
        for i in replies:
            reply = Comment.query.get(i)
            replies_arr.append(reply.comment_to_json())
        return replies_arr

db.create_all()
