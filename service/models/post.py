from django.db import models
from rest_framework import serializers


class Post(models.Model):
    # db_table = 'posts' or service_posts
    title = models.CharField(max_length=140)
    content = models.TextField()
    user = models.ForeignKey(
        on_delete=models.CASCADE, to="User", related_name="Post_users",
    )
    likeUsers = models.ManyToManyField(
        to='User',
        related_name='like_post_users',
        verbose_name='좋아요 선택한 유저목록',
        blank=True,
    )
    hitCount = models.PositiveIntegerField(
        verbose_name='조회수',
        default=0,
        null=True
    )

    def __str__(self):
        return f'{self.title}/{self.id}'
    # is_mine = serializers.SerializerMethodField(read_only=True)


