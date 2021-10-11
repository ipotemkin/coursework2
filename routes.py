from __init__ import *
from flask import render_template, request, redirect
from utils import load_posts_with_comments_count, load_all_data
from errors import NotFoundPostError, NotFoundUserError

HTML_string = "<h2 style=\"color:red\">{}</h2>"


@app.errorhandler(404)
def bad_request_error(error):
    return render_template('error_with_text.html', error_text='Bad request'), 404


@app.errorhandler(NotFoundPostError)
def not_found_post_error(error):
    posts.load()
    return render_template('error_post_not_found.html', posts_count=posts.count()), 404


@app.errorhandler(NotFoundUserError)
def not_found_user_error(error):
    return render_template('error_with_text.html',
                           error_text='Извините, такой пользователь не найден.'), 404


# show all posts
@app.route('/')
def main_feed():
    load_posts_with_comments_count(bkmarks=True)
    return render_template('matrix_view.html',
                           title='SKYPROGRAM',
                           search_mode=True,
                           posts=posts(),
                           bookmarks_count=len(bookmarks())
                           )


# search throughout the posts
@app.route('/search/')
def search():
    load_posts_with_comments_count(bkmarks=True)
    # looking up the posts' content for the word as a substring
    results = posts(entire_word=False, content=word) if (word := request.args.get('s')) else []
    return render_template('search.html',
                           posts=results[:MAX_POSTS_IN_SEARCH],
                           max_posts=len(results),
                           title='SEARCH',
                           search_mode=False,
                           bookmarks_count=len(bookmarks()),
                           searching_word=word
                           )


# one post in detail
@app.route('/posts/<int:uid>')
def post(uid: int):
    load_all_data()
    if post_ := posts(uid):
        post_['comments_count'] = comments.count(post_id=uid)
        post_['bookmarked'] = True if bookmarks.count(pk=uid) else False
        return render_template('post.html',
                               post=post_,
                               comments=comments(post_id=uid),
                               title='POST',
                               search_mode=False,
                               bookmarks_count=len(bookmarks())
                               )
    else:
        raise NotFoundPostError


# show all bookmarks
@app.route('/bookmarks/')
def show_bookmarks():
    bookmarks.load()
    comments.load()
    bookmarks.add_comments_count(comments)  # adding the actual number of comments to each post in the bookmarks
    bookmarks.add_bookmark_status(bookmarks)
    return render_template('matrix_view.html',
                           title='BOOKMARKS',
                           search_mode=False,
                           posts=bookmarks(),
                           bookmarks_count=len(bookmarks())
                           )


# add a bookmark
@app.route('/bookmarks/add/<int:uid>')
def add_bookmark(uid):
    posts.load()
    bookmarks.load()
    if not bookmarks(uid):
        bookmarks.append(posts(uid))
    return redirect(request.referrer)


# delete a bookmark
@app.route('/bookmarks/delete/<int:uid>')
def delete_bookmark(uid):
    bookmarks.load()
    bookmarks.remove(bookmarks(uid))
    return redirect(request.referrer)


# user_feed
@app.route('/users/<user_name>')
def show_user_feed(user_name: str):
    load_posts_with_comments_count(bkmarks=True)
    if not (posts_ := posts(poster_name=user_name)):
        raise NotFoundUserError

    return render_template('matrix_view.html',
                           posts=posts_,
                           title=user_name,
                           search_mode=False,
                           bookmarks_count=len(bookmarks())
                           )


# show tags
@app.route('/tag/<tag>')
def show_tag(tag: str):
    load_posts_with_comments_count(bkmarks=True)
    return render_template('matrix_view.html',
                           posts=posts(entire_word=False, content='#'+tag),
                           title='TAG/' + tag.upper(),
                           search_mode=False,
                           bookmarks_count=len(bookmarks())
                           )


# one post in detail
@app.route('/posts/<int:uid>', methods=['POST'])
def add_comments(uid: int):
    if (new_post_user_name := request.form.get('new_post_user_name')) \
            and (new_comments := request.form.get('new_comments')):
        comments.append(uid, new_post_user_name, new_comments)
        posts(uid)['comments_count'] = comments.count(post_id=uid)
    return render_template('post.html',
                           post=posts(uid),
                           comments=comments(post_id=uid),
                           title='POST',
                           search_mode=False,
                           bookmarks_count=len(bookmarks())
                           )
