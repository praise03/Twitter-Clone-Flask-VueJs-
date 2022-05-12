from config import db
from models import User, Post, Comment


user1 = User(username="praise", email='praise@mail.com')
user1.hash_password("praise")

user2 = User(username="user", email="user@mail.com")
user2.hash_password("user")

user1.following.append(user2)

post1 = Post(body="First post by praise", author=user1)
post2 = Post(body="Second post by praise", author=user1)
post3 = Post(body="First post by User", author=user2)
comment1 = Comment(body="Comment 1", post=post1, author=user1)
reply1 = comment1.add_reply(body="Reply 1", author=user1)
reply2 = comment1.add_reply(body="Reply 2", author=user1)
reply3 = comment1.add_reply(body="Reply 3", author=user2)
reply4 = reply1.add_reply(body="Reply reply 1", author=user2)
reply5 = reply2.add_reply(body="Reply reply 2", author=user2)
db.session.add(user1)
db.session.add(user2)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(comment1)
user1.like_post(post3)
user2.like_post(post2)
user1.like_comment(comment1)
user2.like_comment(reply1)
db.session.commit()

# u = User.query.get(1)
# u2 = User.query.get(2)
# post_arr = []
# for post in Post.query.order_by(Post.id.desc()).all():
#     if u.has_liked(post):
#         post_json = post.post_to_json()
#         post_json['liked'] = 1
#         post_arr.append(post_json)
#     else:
#         post_arr.append(post.post_to_json())
# print(post_arr)
# p = Post(body="A post by praise", author=u)
# p2 = Post(body="Another post by praise", author=u)
# p3 = Post(body="Third post by ..", author=u2)
# p4 = Post(body="A post by ......................", author=u2)
# p5 = Post(body="A post by ......................", author=u2)
# db.session.add(p)
# db.session.add(p2)
# db.session.add(p3)
# db.session.add(p4)
# db.session.add(p5)


# db.session.commit()
# print(token)
# print(User.decode_token(token))