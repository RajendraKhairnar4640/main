from datetime import datetime
from django.test import TestCase
from myapp.models import Post,Comments,Like
from django.contrib.auth.models import User


class TestModel(TestCase):

    @classmethod
    def setUp(self):
        User.objects.create(first_name="raj",username="raj")
        post = Post.objects.create(description="python post",pic="rk1.jpg",user_name_id=1,tags="#programming")
        Comments.objects.create(post_id=post.id,username_id=post.user_name_id,comment="hello python")
        like = Like.objects.create(user_id=1,post_id=1)

    def test_post_data(self):
        post = Post.objects.get(id=1)
        user = User.objects.get(id=1)
        #print("user",user)
        dt = datetime.now()

        self.assertEqual(post.description,"python post")
        self.assertEqual(post.pic,"rk1.jpg")
        self.assertEqual(post.date_posted.date(),dt.date())
        self.assertEqual(post.user_name_id,1)
        self.assertEqual(post.tags,"#programming")

    def test_comment_data(self):
        comment = Comments.objects.get(id=1)
        user = User.objects.get(id=1)
        self.assertEqual(comment.post_id,1)
        self.assertEqual(comment.username_id,user.id)

    def test_like_data(self):
        like = Like.objects.get(id=1)
        user = User.objects.get(id=1)
        post = Post.objects.get(id=1)
        self.assertEqual(like.user_id,user.id)
        self.assertEqual(like.post_id,post.id)