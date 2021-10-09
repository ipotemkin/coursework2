from flask import Flask, render_template, request, redirect
from myclasses import Posts, Bookmarks, Comments


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['OBJ_LIST'] = []


# registers data objects to make some operations on them all
def register_obj(*objects):
    for obj in objects:
        if obj not in app.config['OBJ_LIST']:
            app.config['OBJ_LIST'].append(obj)


MAX_POSTS_IN_SEARCH = 10

# preparing all data objects
posts = Posts('data/data.json')
comments = Comments('data/comments.json')
bookmarks = Bookmarks('data/bookmarks.json')
register_obj(posts, comments, bookmarks)


# a batch script
def load_posts_with_comments_count(bkmarks=False):
    posts.load()  # loading posts from the previously given json file
    comments.load()  # loading comments from the previously given json file
    posts.add_comments_count(comments)  # adding the actual number of comments to each post
    if bkmarks:
        bookmarks.load()
        posts.add_bookmark_status(bookmarks)


def load_all_data():
    for obj in app.config['OBJ_LIST']:
        obj.load()


def wrap_tags(text: str) -> str:
    tag_format = '<a href="/tag/{}" class="item__tag">{}</a>'
    content_lst = []
    if '#' in text:
        for word in text.split():
            if '#' in word:
                word = tag_format.format(word[1:], word)
            content_lst.append(word)
        return ' '.join(content_lst)
    return text


# show all posts
@app.route('/')
def main_feed():
    load_posts_with_comments_count(bkmarks=True)
    return render_template('main.html', posts=posts(), bookmarks_count=len(bookmarks()))


# search throughout the posts
@app.route('/search/')
def search():
    load_posts_with_comments_count(bkmarks=True)
    # looking up the posts' content for the word as a substring
    results = posts(entire_word=False, content=word) if (word := request.args.get('s')) else []
    return render_template('search.html', posts=results[:MAX_POSTS_IN_SEARCH], max_posts=len(results))


# one post in detail
@app.route('/posts/<int:uid>')
def post(uid: int):
    # OPTION 1 - shorter
    # load_posts_with_comments_count(bkmarks=True)
    # return render_template('post.html', post=posts(uid), comments=comments(post_id=uid))

    # OPTION 2, it should be quicker
    load_all_data()
    post_ = posts(uid)
    post_['comments_count'] = comments.count(post_id=uid)
    post_['bookmarked'] = True if bookmarks.count(pk=uid) else False

    # post_['content'] = wrap_tags(post_['content'])  #

    return render_template('post.html', post=post_, comments=comments(post_id=uid))


# show all bookmarks
@app.route('/bookmarks/')
def show_bookmarks():
    bookmarks.load()
    comments.load()
    bookmarks.add_comments_count(comments)  # adding the actual number of comments to each post in the bookmarks
    return render_template('bookmarks.html', bookmarks=bookmarks())


# add a bookmark
@app.route('/bookmarks/add/<int:uid>')
def add_bookmark(uid):
    posts.load()
    bookmarks.load()
    if not bookmarks(uid):
        bookmarks.append(posts(uid))
    return redirect(request.referrer, code=302)


# delete a bookmark
@app.route('/bookmarks/delete/<int:uid>')
def delete_bookmark(uid):
    bookmarks.load()
    bookmarks.remove(bookmarks(uid))
    return redirect(request.referrer, code=302)


# user_feed
@app.route('/users/<user_name>')
def show_user_feed(user_name: str):
    load_posts_with_comments_count(bkmarks=True)
    return render_template('user-feed.html', posts=posts(poster_name=user_name))


# show tags
@app.route('/tag/<tag>')
def show_tag(tag: str):
    load_posts_with_comments_count()
    return render_template('tag.html', posts=posts(entire_word=False, content='#'+tag))


# one post in detail
@app.route('/posts/<int:uid>', methods=['POST'])
def add_comments(uid: int):
    if (new_post_user_name := request.form.get('new_post_user_name')) \
            and (new_comments := request.form.get('new_comments')):
        comments.append(uid, new_post_user_name, new_comments)
        posts(uid)['comments_count'] = comments.count(post_id=uid)
    return render_template('post.html', post=posts(uid), comments=comments(post_id=uid))


if __name__ == '__main__':
    # print(*app.config['OBJ_LIST'], sep='\n')
    app.run()
