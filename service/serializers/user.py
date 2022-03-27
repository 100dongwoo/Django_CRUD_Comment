from service.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "phoneNumber","followUser"
        )
        # exclude = ('password',)
        # fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
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
            "followUser"
        )
        # exclude = ('password',)
        # fields = '__all__'

        # def create(self, validated_data):
        #     password = validated_data.get('password')
        #     user = super().create(validated_data)
        #     user.set_password(password)
        #     user.save()
        #     return user
