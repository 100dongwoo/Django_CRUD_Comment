from service.models import Post
from rest_framework.viewsets import ModelViewSet
from service.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import permissions
from service.permissions import IsOwner

from django.http import HttpResponse, JsonResponse


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


class MyPostView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        get_data = request.data  # or request.GET check both
        # posts_list = (Post.objects.filter(user__id=get_data['id']))
        # posts_list = posts.filter(user__id=request.data["id"])
        posts_list = Post.objects.filter(user__id=request.session.get("_auth_user_id"))
        serialized_posts = PostSerializer(posts_list, many=True,context={"request": request})
        return Response(data=serialized_posts.data)
        
        #  posts_list= posts.filter(user__id=request.data["id"])
        # return JsonResponse({"data": posts_list})

        # @api_view(["GET"])
        # def list_rooms(request):
        #     rooms = Room.objects.all()
        #     serialized_rooms = RoomSerializer(rooms, many=True)
        #     return Response(data=serialized_rooms.data)

        # # serializer = PostSerializer(data=posts_list, many=True)
        # #
        # # posts_list = (Post.objects.filter(user__id=get_data['id']))
        # serializer = PostSerializer(data=posts_list, many=True)
        #
        # if serializer.is_valid():
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_502_BAD_GATEWAY)

        # return JsonResponse({'ok': True, 'status': 200, 'msg': '테스트다.'}, status=200)

    # def get(self, request):
    # posts = Post.objects.all()
    # data = posts.filter(user__id=request.session.get("_auth_user_id"))
    # serializer = PostSerializer(data=data)
    # print(data)
    # if serializer.is_valid():
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
