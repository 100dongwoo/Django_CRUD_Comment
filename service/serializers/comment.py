from rest_framework import serializers
from service.models import Comment
from service.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'created_at', 'comment', "user"]


class DetailCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ["is_mine", 'id', 'post', 'user', 'created_at', 'comment', "user"]

    def get_is_mine(self, obj):
        me = self.context['request'].user
        if not me.is_authenticated:
            return False
        return obj.user_id == me.id
