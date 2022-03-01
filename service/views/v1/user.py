from service.models import User
from rest_framework.viewsets import ModelViewSet
from service.serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignUpView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserProfileSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if 'password' in data:
                new_user.set_password(data['password'])
            else:
                return Response({'msg': 'password not exist'}, status=403)
            new_user.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )
