import json


class DBase:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def __call__(self, uid=None, **kwargs):
        if not kwargs:
            return self.data if not uid else self.get_item_by_id(uid)
        return self.get_items(**kwargs)

    def load(self):
        with open(self.filename, encoding='utf-8') as fp:
            self.data = json.load(fp)

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as fp:
            json.dump(self.data, fp, ensure_ascii=False, indent='\t')

    def get_item_by_id(self, uid: int):
        for item in self.data:
            if item['pk'] == uid:
                return item
        return []

    def get_items_by_user(self, user: str):
        return [item for item in self.data if item['poster_name'] == user]

    def get_items(self, **kwargs):
        kwargs_dict = {**kwargs}
        key = list(kwargs_dict.keys())[0]
        value = list(kwargs_dict.values())[0]
        return [item for item in self.data if item[key] == value]

    def add_comments_count(self, comments: 'DBase'):
        for post in self.data:
            print(post['pk'])
            post['comments_count'] = comments.count(post_id=post['pk'])

    def count(self, **kwargs):
        if not kwargs:
            return 0
        kwargs_dict = {**kwargs}
        key = list(kwargs_dict.keys())[0]
        value = list(kwargs_dict.values())[0]
        return len([item for item in self.data if item[key] == value])

# posts = DBase('data/data.json')
# posts.load()
# # print(posts())
# # print(posts(1))
# print(posts.get_items(pk=2))
# print(posts(pk=2))
# print(posts.count(poster_name='leo'))
# comments = DBase('data/comments.json')
# comments.load()
# print(comments())
# posts.add_comments_count(comments)
# print(posts())
