from flask import Flask, jsonify, request
from models import User, Post, Comment
from config import app, db
from auth import token_required


@app.route('/api/signup/', methods=['POST'])
def signup():
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'must include username, email and password fields'})
    username = data['username']
    email = data['email']
    password = data['password']
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already in use. Kindly choose another.'})
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already in use. Kindly choose another.'})
    new_user = User(username=username, email=email)
    new_user.hash_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account Created Successfully', 'status': 'ok'})


@app.route('/api/signin/', methods=['POST'])
def signin():
    data = request.get_json()
    if 'usernameOrEmail' not in data or 'password' not in data:
        return jsonify({'error': 'must include username, email and password fields', 'data': data})
    user = data['usernameOrEmail']
    password = data['password']
    if User.query.filter_by(username=user).first():
        user = User.query.filter_by(username=user).first()
    elif User.query.filter_by(email=user).first():
        user = User.query.filter_by(email=user).first()
    else:
        return jsonify({'error': 'Incorrect credentials. Kindly try again'})
    if user.verify_password(password):
        token = user.generate_token()
        return jsonify({'message': 'Login Successful', 'token': token, 'user': user.user_to_json()})
    else:
        return jsonify({'error': 'Login Failed'})


@app.route('/api/fetch/feed', methods=['GET', 'POST'])
def fetch_all_posts():
    if request.method == 'GET':
        post_arr = []
        for post in Post.query.order_by(Post.id.desc()).all():
            post_arr.append(post.post_to_json())
        return jsonify(post_arr)
    elif 'user' in request.get_json():
        user = User.query.get(request.get_json()['user'])
        post_arr = []
        for post in Post.query.order_by(Post.id.desc()).all():
            if user.has_liked_post(post):
                post_json = post.post_to_json()
                post_json['liked'] = 1
                post_arr.append(post_json)
            else:
                post_arr.append(post.post_to_json())
        return jsonify(post_arr)
    else:
        post_arr = []
        for post in Post.query.order_by(Post.id.desc()).all():
            post_arr.append(post.post_to_json())
        return jsonify(post_arr)


@app.route('/api/fetch/post', methods=['GET', 'POST'])
def fetch_post():
    post_id = request.get_json()['post_id']
    post = Post.query.get(post_id)
    post_json = post.post_to_json()
    if 'user' in request.get_json():
        print(request.get_json())
        user = User.query.get(request.get_json()['user'])
        for comment in post_json['comments']:
            if user.has_liked_comment(Comment.query.get(comment['id'])):
                comment['liked'] = True
        return post_json
    else:
        return post_json

# @app.route('/api/fetch/comments', methods=['POST'])
# def fetch_comments():
#     post_id = request.get_data()
#     print(post_id)
#     return post_id


@app.route('/api/fetch/replies', methods=['POST'])
def fetch_replies():
    comment_id = request.get_data().decode()
    if not comment_id:
        return ' '
    print(comment_id)
    comment = Comment.query.get_or_404(comment_id)
    replies = comment.get_replies()
    return jsonify({'comment': comment.comment_to_json(), 'replies': replies})


@app.route('/api/tweet/create', methods=['POST', 'OPTIONS'])
@token_required
def create_post():
    data = request.get_json()
    user = User.query.get_or_404(data['author'])
    body = data['body']
    post = Post(body=body, author=user)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'success'})


@app.route('/api/tweet/like', methods=['POST', 'OPTIONS'])
@token_required
def like_post():
    data = request.get_json()
    user = User.query.get_or_404(data['user'])
    post_id = data['tweet']
    post = Post.query.get(post_id)
    if user.has_liked_post(post):
        user.unlike_post(post)
    else:
        user.like_post(post)
    db.session.commit()
    return jsonify({'message': 'done'})


@app.route('/api/tweet/comment', methods=['POST', 'OPTIONS'])
@token_required
def comment():
    data = request.get_json()
    user = User.query.get_or_404(data['author'])
    post_id = data['tweet']
    post = Post.query.get(post_id)
    c = Comment(body=data['body'], post=post, author=user)
    db.session.add(c)
    db.session.commit()
    return jsonify({'message': 'success'})


@app.route('/api/comment/like', methods=['POST', 'OPTIONS'])
@token_required
def like_comment():
    data = request.get_json()
    user = User.query.get_or_404(data['user'])
    comment_id = data['comment']
    comment = Comment.query.get(comment_id)
    if user.has_liked_comment(comment):
        user.unlike_comment(comment)
    else:
        user.like_comment(comment)
    db.session.commit()
    return jsonify({'message': 'done'})


@app.route('/api/token/validate', methods=['GET', 'POST'])
def validate_token():
    token = request.get_json()['token']
    print('Here')
    validity = User.decode_token(token)
    if validity == 'Token Expired':
        user_id = request.get_json()['user_id']
        user = User.query.get_or_404(user_id)
        return jsonify({'token': user.generate_token()})
    elif validity == 'Invalid Token':
        return jsonify({'message': 'Invalid Token'})
    else:
        return jsonify({'message': 'Valid Token'})


@app.route('/api/token/generate', methods=['POST'])
def generate_token():
    user_id = request.get_json()['user_id']
    user = User.query.get_or_404(user_id)
    return jsonify({'token': user.generate_token()})


@app.route('/api/user/profile', methods=['POST'])
def get_user_profile():
    username = request.get_json()['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'user not found'})
    post_arr = []
    for post in user.posts:
        post_arr.append(post.post_to_json())
    return jsonify({
        'user': user.user_to_json(),
        'posts': post_arr
    })


@app.route('/api/user/following', methods=['POST'])
def check_following():
    username = request.get_json()['user']
    user = User.query.filter_by(username=username).first()
    current_user = User.query.get(request.get_json()['current_user'])
    if current_user.is_following(user):
        return jsonify({'following': 'true'})
    else:
        return jsonify({'following': 'false'})


@app.route('/api/user/follow', methods=['POST'])
def follow():
    username = request.get_json()['user']
    user = User.query.filter_by(username=username).first()
    current_user = User.query.get(request.get_json()['current_user'])
    current_user.follow(user)
    db.session.commit()
    return jsonify({'message': 'done'})


@app.route('/api/user/unfollow', methods=['POST'])
def unfollow():
    username = request.get_json()['user']
    user = User.query.filter_by(username=username).first()
    current_user = User.query.get(request.get_json()['current_user'])
    current_user.unfollow(user)
    db.session.commit()
    return jsonify({'message': 'done'})


@app.route('/api/test', methods=['GET', 'POST'])
@token_required
def re():
    return jsonify({'done': 'yes'})
