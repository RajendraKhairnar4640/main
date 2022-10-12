from django.urls import path
from . import views 
from rest_framework_simplejwt.views import  TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('postapi/',views.PostAPI.as_view(),name='postapi'),
    path('postapi/<int:post_id>/',views.PostAPI.as_view(),name='postid'),
    path("commentapi/",views.CommentAPI.as_view()),

    path('api-login/', TokenObtainPairView.as_view(), name='login_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('api-register/',views.RegisterAPIView.as_view(),name='api-register'),
    path('commentapi/',views.CommentAPI.as_view()),
    path('commentapi/<int:pk>/',views.CommentAPI.as_view()),

    path('likeapi/',views.LikeAPI.as_view()),


 
]
