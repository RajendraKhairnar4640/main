from django.contrib import admin
from .models import Post,Comments,Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','description','pic','date_posted','user_name','tags']

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','username','comment','comment_date']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','post']

