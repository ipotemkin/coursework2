from flask import Flask, render_template, request, redirect
from dbase import DBase


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# POSTS_FILE_NAME = 'data/data.json'
# COMMENTS_FILE_NAME = 'data/comments.json'
# BOOKMARKS_FILE_NAME = 'data/bookmarks.json'
MAX_POSTS_IN_SEARCH = 10
posts = DBase('data/data.json')
comments = DBase('data/comments.json')
bookmarks = DBase('data/bookmarks.json')


# def read_json(filename):
#     with open(filename, encoding='utf-8') as fp:
#         return json.load(fp)
#
#
# def to_json(filename, what):
#     with open(filename, 'w', encoding='utf-8') as fp:
#         json.dump(what, fp, ensure_ascii=False, indent='\t')
#
#
# def get_post_by_id(uid: int, posts):
#     for post in posts:
#         if post['pk'] == uid:
#             return post
#     return []
#
#
# def get_posts_by_user(user: str, posts):
#     return [post for post in posts if post['poster_name'] == user]
#
#
# def get_comments_by_post_id(post_id: int, comments=None):
#     if not comments:
#         comments = read_json(COMMENTS_FILE_NAME)
#     return [comment for comment in comments if comment['post_id'] == post_id]
#
#
# def add_comments_count_to_posts(posts, comments):
#     for post in posts:
#         post['comments_count'] = len(get_comments_by_post_id(post['pk'], comments))
#     return posts


def load_posts_with_comments_count():
    global posts, comments
    posts.load()
    comments.load()
    posts.add_comments_count(comments)
    return posts


# all posts
@app.route('/')
def main_feed():
    # posts.load()
    # comments.load()
    # posts.add_comments_count(comments)
    global posts
    posts = load_posts_with_comments_count()
    return render_template('main.html', posts=posts())


# search throughout the posts
@app.route('/search/')
def search():
    global posts
    posts = load_posts_with_comments_count()
    results = []
    if word := request.args.get('s'):
        word = word.lower()
        results = [post for post in posts() if word in post['content'].lower()]
    return render_template('search.html', posts=results[:MAX_POSTS_IN_SEARCH], max_posts=len(results))


# one post in detail
@app.route('/posts/<int:uid>')
def post(uid: int):
    posts.load()
    comments.load()
    return render_template('post.html', post=posts(uid), comments=comments(post_id=uid))


# show bookmarks
@app.route('/bookmarks/')
def show_bookmarks():
    bookmarks.load()
    comments.load()
    bookmarks.add_comments_count(comments)
    return render_template('bookmarks.html', bookmarks=bookmarks())


# add a bookmark
@app.route('/bookmarks/add/<int:uid>')
def add_bookmark(uid):
    posts.load()
    bookmarks.load()
    if not bookmarks(uid):
        bookmarks.data.append(posts(uid))
        bookmarks.save()
    return redirect('/')


# delete a bookmark
@app.route('/bookmarks/delete/<int:uid>')
def delete_bookmark(uid):
    bookmarks.load()
    bookmarks.data.remove(bookmarks(uid))
    bookmarks.save()
    return redirect('/bookmarks/')


# user_feed
@app.route('/users/<user_name>')
def show_user_feed(user_name: str):
    global posts
    posts = load_posts_with_comments_count()
    return render_template('user-feed.html', posts=posts(poster_name=user_name))


if __name__ == '__main__':
    app.run()
