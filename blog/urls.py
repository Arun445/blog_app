from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, AddCommentToPostView, CommentRemoveView
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment', AddCommentToPostView.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/delete', CommentRemoveView.as_view(), name='comment_remove'),
    path('comment/<int:pk>/approve', views.comment_approve, name='comment_approve'),
]