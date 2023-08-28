from rest_framework import serializers

from post.models import Post, Comment
from post.utils import get_author


class CommentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "content", "created_at", "created_by")

    @staticmethod
    def get_created_by(instance) -> str:
        return get_author(instance)


class CommentListSerializer(CommentSerializer):
    class Meta(CommentSerializer.Meta):
        read_only_fields = fields = (
            "id",
            "content",
            "created_at",
            "created_by",
        )


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source="likes.count", read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "created_at",
            "created_by",
            "likes",
            "comments",
        )
        read_only_fields = (
            "id",
            "content",
            "created_at",
            "created_by",
            "likes",
            "comments",
        )

    @staticmethod
    def get_created_by(instance) -> str:
        return get_author(instance)


class PostUpdateSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "created_at",
            "created_by",
            "likes",
            "comments",
        )


class PostListSerializer(PostSerializer):
    comments = serializers.IntegerField(
        source="comments.count", read_only=True
    )

    class Meta(PostSerializer.Meta):
        model = Post
        fields = (
            "id",
            "content",
            "created_at",
            "created_by",
            "likes",
            "comments",
        )
        read_only_fields = (
            "id",
            "content",
            "created_at",
            "created_by",
            "likes",
            "comments",
        )
