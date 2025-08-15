from django.contrib import admin
from .models import Post,Category,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author','title','date_posted'] 
    filter_horizontal = ['like']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','name','created_at'] 

