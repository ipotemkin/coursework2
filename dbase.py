import json


class DBase:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def __call__(self, uid=None, entire_word=True, case_sensitive=False, **kwargs):
        """
        A universal function to get the stored data
        Option 1: object() - returns all data
        Option 2: object(uid) - returns an item with the given uid
        Option 3: object(field_name=value) - returns a list of items that meet the required argument
        You can also differentiate your search changing entire_word or/and case_insensitive
        If you set entire_word=True the function searches only an entire word match
        If you set entire_word=False the function searches the given value as a substring of the given field_name
        """
        if not kwargs:
            return self.data if not uid else self.get_item_by_id(uid)
        return self.get_items(entire_word, case_sensitive, **kwargs)

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

    def get_items(self, entire_word=True, case_sensitive=False, **kwargs):
        kwargs_dict = {**kwargs}
        key = list(kwargs_dict.keys())[0]
        value = list(kwargs_dict.values())[0]
        if not case_sensitive:
            value = str(value).lower()
        if entire_word:
            return [item for item in self.data if (item[key] if case_sensitive else str(item[key]).lower()) == value]
        return [item for item in self.data if value in (item[key] if case_sensitive else str(item[key]).lower())]

    def add_comments_count(self, comments: 'DBase'):
        for post in self.data:
            post['comments_count'] = comments.count(post_id=post['pk'])

    def add_bookmark_status(self, bookmarks: 'DBase'):
        for post in self.data:
            post['bookmarked'] = True if bookmarks(post['pk']) else False

    def count(self, **kwargs):
        if not kwargs:
            return 0
        kwargs_dict = {**kwargs}
        key = list(kwargs_dict.keys())[0]
        value = list(kwargs_dict.values())[0]
        return len([item for item in self.data if item[key] == value])

    def get_max_id(self):
        max_id = 0
        for item in self.data:
            if max_id < item['pk']:
                max_id = item['pk']
        return max_id

    def append(self, item):
        self.data.append(item)
        self.save()

# it doesn't work in html
#     def wrap_tags(self):
#         field = 'content'
#         tag_format = '<a href="/tag/{}">{}</a>'
#         content_lst = []
#         for item in self.data:
#             if '#' in item[field]:
#                 for word in item[field].split():
#                     if '#' in word:
#                         word = tag_format.format(word[1:], word)
#                     content_lst.append(word)
#                 item[field] = ' '.join(content_lst)


class Comments(DBase):
    def append(self, post_id: int, commenter_name: str, comment: str):
        self.load()
        self.data.append({'post_id': post_id,
                          'commenter_name': commenter_name,
                          'comment': comment,
                          'pk': self.get_max_id() + 1})
        self.save()


if __name__ == '__main__':
    posts = DBase('data/data.json')
    posts.load()
    print(posts(entire_word=False, content='#инста'))
    # posts.wrap_tags()
    # print(posts(5))
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
