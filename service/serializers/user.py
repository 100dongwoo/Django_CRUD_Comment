from service.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    follow_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "phoneNumber",
            "followUser",
            'follow_count'
        )
        # exclude = ('password',)
        # fields = '__all__'

    def get_follow_count(self, obj):
        return len(obj.followUser.all())


class UserProfileSerializer(serializers.ModelSerializer):
    follow_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "phoneNumber",
            "followUser",
            'follow_count'
        )

        def get_follow_count(self, obj):
            return len(obj.followUser.all())
        # exclude = ('password',)
        # fields = '__all__'

        # def create(self, validated_data):
        #     password = validated_data.get('password')
        #     user = super().create(validated_data)
        #     user.set_password(password)
        #     user.save()
        #     return user
