class User(object):
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        self.posts = []
        self.following = []

    def add_post(self, post):
        post.set_user(self)
        self.posts.append(post)

    def get_timeline(self):
        timeline_posts = []
        for user in self.following:
            timeline_posts += user.posts

        return sorted(timeline_posts, key = lambda post: post.timestamp)

    def follow(self, other):
        self.following.append(other)