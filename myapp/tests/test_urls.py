from django.test import SimpleTestCase
from django.urls import reverse, resolve
from myapp.views import PostListView,RegisterView,LoginView,user_dashboard,create_post,post_detail,like,search_posts,post_delete,UserPostListView
from django.contrib.auth.views import LogoutView


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        #print(resolve(url))
        self.assertEqual(resolve(url).func.view_class,PostListView)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class,RegisterView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class,LoginView)

    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func,user_dashboard)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class,LogoutView)

    def test_postcreate_url_is_resolved(self):
        url = reverse('post-create')
        self.assertEqual(resolve(url).func,create_post)

    def test_postdetail_url_is_resolved(self):
        url = reverse('post-detail',args=[1])
        self.assertEqual(resolve(url).func,post_detail)

    def test_like_url_is_resolved(self):
        url = reverse('post-like')
        self.assertEqual(resolve(url).func,like)

    def test_searchpost_is_resolved(self):
        url = reverse('search_posts')
        self.assertEqual(resolve(url).func,search_posts)

    def test_postdelete_is_resolved(self):
        url = reverse('post-delete',args=[1])
        self.assertEqual(resolve(url).func,post_delete)

    def test_userposts_is_resolved(self):
        url = reverse('user-posts',args=['raj'])
        self.assertEqual(resolve(url).func.view_class,UserPostListView)

