from django.urls import path

from post.views import (
    PostCreateView,
    FeedView,
    PostRetrieveView,
    LikePostView,
    LikedPostsView,
)

urlpatterns = [
    path("new-post/", PostCreateView.as_view(), name="new-post"),
    path(
        "post-details/<int:post_id>/",
        PostRetrieveView.as_view(),
        name="post-detail",
    ),
    path(
        "post-details/<int:post_id>/like/",
        LikePostView.as_view(),
        name="like-unlike-post",
    ),
    path("feed/", FeedView.as_view(), name="feed"),
    path("liked-posts/", LikedPostsView.as_view(), name="liked-posts"),
]

app_name = "post"
