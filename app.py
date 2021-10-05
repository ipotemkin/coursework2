from flask import Flask, render_template, request
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

POSTS_FILE_NAME = 'data/data.json'
MAX_POSTS_IN_SEARCH = 10


def load_posts(filename):
    with open(filename, encoding='utf-8') as fp:
        return json.load(fp)


def get_post_by_id(uid: int, posts):
    for post in posts:
        if post['id'] == uid:
            return post
    raise IndexError


# all posts
@app.route('/')
def main_feed():
    return render_template('main.html', posts=load_posts(POSTS_FILE_NAME))


# search throughout the posts
@app.route('/search/')
def search():
    posts = load_posts(POSTS_FILE_NAME)
    results = []
    if word := request.args.get('s'):
        word = word.lower()
        results = [post for post in posts if word in post['content'].lower()]
    return render_template('search.html', posts=results[:MAX_POSTS_IN_SEARCH], max_posts=len(results))


# one post in detail
@app.route('/posts/<int:uid>')
def post(uid: int):
    posts = load_posts(POSTS_FILE_NAME)
    post = get_post_by_id(uid, posts)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run()
