from django.urls import path
from . import views
from .views import PostListView,UserPostListView,RegisterView,LoginView
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    #path('register/',views.register,name='register'),
    path('register/',RegisterView.as_view(),name='register'),
    #path('login/',views.user_login,name='login'),
    path("login/", LoginView.as_view(), name="login"),
    path('dashboard/',views.user_dashboard,name='dashboard'),
    #path('logout/',views.user_logout,name='logout'),
    path('logout/',LogoutView.as_view(next_page='home'),name='logout'),
    path('post/new/',views.create_post,name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('like/', views.like, name='post-like'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('user_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),

]