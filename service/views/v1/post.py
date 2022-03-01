from service.models import Post
from rest_framework.viewsets import ModelViewSet
from service.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
