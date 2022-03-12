from service.models import Post
from rest_framework import serializers
from service.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

        # fields = ( "content", )
        # exclude = ("created",)
        # read_only_fields = ["user", "id", "created", "updated", ]

    def get_is_mine(self, obj):
        me = self.context['request'].user
        if not me.is_authenticated:
            return False
        return obj.user_id == me.id