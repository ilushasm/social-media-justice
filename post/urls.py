from django.urls import path

from post.views import PostCreateView, FeedView, PostRetrieveView, LikePostView

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
]

app_name = "post"
