from django.urls import path

from .views import (
    HomePageView,
    PostCreateView,
    PostDetailView,
    CommentCreateView,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_pk>/add-comment', CommentCreateView.as_view(), name='comment_add')
]
