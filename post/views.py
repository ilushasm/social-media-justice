from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet

from post.models import Post
from post.serializers import PostSerializer
from user.models import Follow


class PostCreateView(generics.CreateAPIView):
    """Creates new Post instance"""

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        serializer.save(created_by=self.request.user)


class FeedView(generics.ListAPIView):
    """Returns all posts made by logged-in user and user's followed by logged-in user"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        queryset = self.queryset

        followed_users = Follow.objects.filter(follower=user).values_list(
            "user", flat=True
        )
        queryset = queryset.filter(created_by__in=followed_users)

        return queryset
