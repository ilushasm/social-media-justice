from typing import Type

from rest_framework import generics, views, status
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import QuerySet

from post.models import Post, Like, Comment
from post.serializers import (
    PostSerializer,
    PostUpdateSerializer,
    PostListSerializer,
    CommentSerializer,
    CommentListSerializer,
)
from post.utils import get_like_object


class PostCreateView(generics.CreateAPIView):
    """Creates new Post instance"""

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        serializer.save(created_by=self.request.user)


class PostRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns Post Detail page. If post was created by logged-in user uses PostUpdateSerializer,
    that allows updating
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self) -> Post:
        queryset = self.queryset
        post_id = self.kwargs["post_id"]
        post = queryset.get(id=post_id)
        return post

    def get_serializer_class(self) -> Type[Serializer]:
        post = self.get_object()
        user = self.request.user
        if post.created_by == user:
            return PostUpdateSerializer
        return PostSerializer


class FeedView(generics.ListAPIView):
    """
    Returns all posts made by logged-in user and user's followed by logged-in user
    IF NO SEARCH PARAMETERS ARE GIVEN. If parameters are give it returns all Post filtered
    by given search parameters
    """

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        queryset = self.queryset
        filter_params = self.request.query_params

        if not filter_params:
            followed_users = user.following.values_list("user", flat=True)
            queryset = queryset.filter(created_by__in=followed_users)

        else:
            content = filter_params.get("content")
            created_at = filter_params.get("created_at")

            if content:
                queryset = queryset.filter(content__icontains=content)

            if created_at:
                queryset = queryset.filter(created_at__date=created_at)

        return queryset


class LikePostView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, post_id: int) -> Response:
        user = request.user
        like = get_like_object(post_id=post_id, user_id=user.id)

        if like is None:
            Like.objects.create(post_id=post_id, created_by=user)
            return Response(
                {"message": "You have liked this post"},
                status=status.HTTP_200_OK,
            )
        like.delete()
        return Response(
            {"message": "You have unliked this post"},
            status=status.HTTP_404_NOT_FOUND,
        )


class LikedPostsView(generics.ListAPIView):
    """Returns list of all posts liked by current user"""

    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PostListSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        user = self.request.user
        liked_posts = user.likes.values_list("post", flat=True)

        queryset = queryset.filter(id__in=liked_posts)
        return queryset


class CommentCreateView(generics.CreateAPIView):
    """Provides functionality to Create Comment instance"""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        post_id = self.kwargs["post_id"]
        serializer.save(created_by=self.request.user, post_id=post_id)


class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Provides functionality to Update or Delete Comment instance"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> Comment:
        comment_id = self.kwargs["comment_id"]
        return Comment.objects.get(id=comment_id)

    def get_serializer_class(self) -> Type[Serializer]:
        user = self.request.user
        comment = self.get_object()
        if comment.created_by == user:
            return CommentSerializer
        return CommentListSerializer
