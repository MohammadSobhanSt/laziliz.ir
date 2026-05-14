from django.urls import path
from . import views



app_name = 'blogs'
urlpatterns = [
    path('my-blogs/', views.UserBlogView.as_view(), name='my-blogs'),
    path('create/', views.CreateBlogView.as_view(), name='blogs-create'),
    path('create/comment/', views.CreateCommentView.as_view(), name='comments-create'),
    path('detail/<slug:blog_slug>/', views.BlogDetailView.as_view(), name='blogs-detail'),
    path('like/<slug:blog_slug>/', views.BlogLikeView.as_view(), name='blogs-like'),
    path('unlike/<slug:blog_slug>/', views.BlogUnlikeView.as_view(), name='blogs-unlike'),
    path('update/<slug:blog_slug>/', views.UpdateBlogView.as_view(), name='blogs-update'),
    path('delete/<slug:blog_slug>/', views.DeleteBlogView.as_view(), name='blogs-delete'),
]