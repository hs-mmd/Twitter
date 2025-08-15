from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailsView.as_view(), name='post_detail'),
    path('create-post/', views.CreatePostView.as_view(), name='create_post'),
    path('update-post/<int:pk>/', views.UpdatePostView.as_view(), name='update_post'),
    path('delete-post/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('like-post/<int:pk>/', views.like_view, name='like_post'),
    path('create-category/', views.CreatCategoryView.as_view(), name='create_category'),
    path('list-category/', views.ListCategoryView.as_view(), name='list_category'),
    path('category/<str:cat>/', views.category_view, name='category'),
    path('post/<int:pk>/comment', views.CreateComment.as_view(), name='create_comment'),
    path('category/<int:pk>/subscribe/',   views.subscribe_category,   name='subscribe_category'),
    path('category/<int:pk>/unsubscribe/', views.unsubscribe_category, name='unsubscribe_category'),
    path('feed/categories/', views.CategoryFeedView.as_view(), name='category_feed'),
    path('post/<int:pk>/archive/',   views.archive_post,   name='post_archive'),
    path('post/<int:pk>/unarchive/', views.unarchive_post, name='post_unarchive'),


]
