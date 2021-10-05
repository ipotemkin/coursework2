from flask import Flask, render_template, request
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

POSTS_FILE_NAME = 'data/data.json'
COMMENTS_FILE_NAME = 'data/comments.json'
MAX_POSTS_IN_SEARCH = 10


def read_json(filename):
    with open(filename, encoding='utf-8') as fp:
        return json.load(fp)


def get_post_by_id(uid: int, posts):
    for post in posts:
        if post['pk'] == uid:
            return post
    raise IndexError


def get_comments_by_post_id(post_id: int):
    comments = read_json(COMMENTS_FILE_NAME)
    return [comment for comment in comments if comment['post_id'] == post_id]


# all posts
@app.route('/')
def main_feed():
    return render_template('main.html', posts=read_json(POSTS_FILE_NAME))


# search throughout the posts
@app.route('/search/')
def search():
    posts = read_json(POSTS_FILE_NAME)
    results = []
    if word := request.args.get('s'):
        word = word.lower()
        results = [post for post in posts if word in post['content'].lower()]
    return render_template('search.html', posts=results[:MAX_POSTS_IN_SEARCH], max_posts=len(results))


# one post in detail
@app.route('/posts/<int:uid>')
def post(uid: int):
    posts = read_json(POSTS_FILE_NAME)
    post = get_post_by_id(uid, posts)
    return render_template('post.html', post=post, comments=get_comments_by_post_id(uid))


if __name__ == '__main__':
    app.run()
