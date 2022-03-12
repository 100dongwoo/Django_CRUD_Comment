from service.models import Post
from rest_framework import serializers
from service.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    # is_readyLike = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id", "title", "content", "user", "is_mine", "like_count"
        )

        # fields = ( "content", )
        # exclude = ("created",)
        # read_only_fields = ["user", "id", "created", "updated", ]

    def get_is_mine(self, obj):
        me = self.context['request'].user
        if not me.is_authenticated:
            return False
        return obj.user_id == me.id

    def get_like_count(self, obj):
        return len(obj.likeUsers.all())

    # def get_is_readyLike(self, obj):
    #     me = self.context['request'].user

        # if not me.is_authenticated:
        #     return False
        # else:
        #     if obj.likeUsers.all() in me:
        #         return True
        #     else:
        #         return False

        #     else:
        #         return False
        # return obj.likeUsers.all() in me

        # me = self.context['request'].user
        # if obj.likeUsers in me:
        #     return True
        # else:
        #     return False
