from __init__ import app, posts, comments, bookmarks


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
