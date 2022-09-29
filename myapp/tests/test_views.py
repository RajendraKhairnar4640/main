from django.test import TestCase
from myapp.models import Post
from django.test import Client
from django.urls import reverse

class PostViewTestClass(TestCase):
    def create_post(self,description='first post',tags="social",pic="rk1.jpg"):
        return Post.objects.create(description=description,tags=tags,pic=pic)

    def test_post_create(self):
        obj = self.create_post(description="second post")
        post_url = reverse("post-create")
        print(post_url)
        response = self.client.get(post_url)
        self.assertTrue(response.status_code,200)

