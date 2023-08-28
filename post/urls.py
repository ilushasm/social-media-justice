from django.urls import path

from post.views import PostCreateView, FeedView


urlpatterns = [
    path("new-post/", PostCreateView.as_view(), name="new-post"),
    path("feed/", FeedView.as_view(), name="feed"),
]

app_name = "post"
