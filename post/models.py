from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), related_name="posts", on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), related_name="comments", on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    created_by = models.ForeignKey(get_user_model(), related_name="likes", on_delete=models.CASCADE)
