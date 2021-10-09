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
