from service.models import Post
from rest_framework.viewsets import ModelViewSet
from service.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import permissions
from service.permissions import IsOwner


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            # permission_classes = [permissions.AllowAny]
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class MyPostView(APIView):
#
#     def get(self, request):
#         posts = Post.objects.all()
#         # user = User.objects.filter(email=input_data['email']).first()
#         print(posts.filter(user=request.session["_auth_user_id"]))
#         # for key, value in request.session.items():
#         #     print('{} => {}'.format(key, value))
#         return Response({'response': 'ok'})  # 에러 없이 수행됐을 시의 결과 출력
