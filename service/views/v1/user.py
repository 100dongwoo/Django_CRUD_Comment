from service.models import User
from rest_framework.viewsets import ModelViewSet
from service.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
