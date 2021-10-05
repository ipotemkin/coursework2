from flask import Flask, render_template
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

POSTS_FILE_NAME = 'data/data.json'


def load_posts(filename):
    with open(filename, encoding='utf-8') as fp:
        return json.load(fp)


@app.route('/')
def main_feed():
    return render_template('main.html', posts=load_posts(POSTS_FILE_NAME))


if __name__ == '__main__':
    app.run()
