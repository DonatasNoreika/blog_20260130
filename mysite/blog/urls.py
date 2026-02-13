from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name="posts"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post"),
    path('search/', views.search, name='search'),
    path("userposts/", views.UserPostListView.as_view(), name="userposts"),
    path("usercomments/", views.UserCommentListView.as_view(), name="usercomments"),
    path("profile/", views.profile, name="profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('posts/create/', views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
]
