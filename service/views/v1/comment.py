from service.models import Comment
from service.serializers import CommentSerializer
from rest_framework.viewsets import ModelViewSet
from django.db import transaction

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)