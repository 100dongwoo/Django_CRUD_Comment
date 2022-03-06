from rest_framework import serializers
from service.models import Comment
from service.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'created_at', 'comment', "user"]
