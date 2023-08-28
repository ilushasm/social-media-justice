from rest_framework import serializers

from post.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source="likes.count")

    class Meta:
        model = Post
        fields = ("id", "content", "created_at", "created_by", "likes")

    @staticmethod
    def get_created_by(instance) -> str:
        if (
            instance.created_by.first_name is not None
            and instance.created_by.last_name is not None
        ):
            return (
                f"{instance.created_by.first_name} {instance.created_by.last_name} (@{instance.created_by.username})"
            )
        return f"@{instance.created_by.username}"
