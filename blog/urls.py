from django.urls import path
from . import views 
from .views import(
     PostListView , 
     PostDetailView,
     PostCreateView, 
     PostUpdateView,
     PostDeleteView, 
     UserPostListView,
     LikeView,
     DisLikeView,
     CommentDeleteView,
)

urlpatterns = [
    
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.About, name='blog-about'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('dislike/<int:pk>',DisLikeView,name='dislike_post'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]
