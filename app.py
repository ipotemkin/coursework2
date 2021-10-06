from flask import Flask, render_template, request, redirect
from dbase import DBase


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

MAX_POSTS_IN_SEARCH = 10
posts = DBase('data/data.json')
comments = DBase('data/comments.json')
bookmarks = DBase('data/bookmarks.json')


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
    # posts.wrap_tags()
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
    return redirect('/#post'+str(uid))


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


# show tags
@app.route('/tag/<tag>')
def show_tag(tag: str):
    global posts
    posts = load_posts_with_comments_count()
    return render_template('tag.html', posts=posts(entire_word=False, content='#'+tag))


if __name__ == '__main__':
    app.run()
