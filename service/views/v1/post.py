from service.models import Post, Comment, User
from rest_framework.viewsets import ModelViewSet
from service.serializers import PostSerializer, FollowerPostSerializer, DetailCommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import permissions
from service.permissions import IsOwner
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        postId = serializer.data["id"]
        # comments = Comment.objects.all()
        # comments_list = comments.filter(post=postId)
        comments = Comment.objects.select_related('user', 'post').filter(post=postId).order_by('-created_at').distinct()
        serializer_comments = DetailCommentSerializer(comments, many=True, context={"request": request})

        instance.hitCount += 1
        instance.save()

        return JsonResponse({'post': serializer.data, "comment": serializer_comments.data}, status=200)
        # return Response(serializer.data)

    #
    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @transaction.atomic()
    @action(detail=False, methods=["post"])
    def toggleLike(self, request):
        data = request.data
        # post = Post.objects.get(id=data["id"])
        # if post is not None:
        if request.user.is_anonymous:
            return JsonResponse({"msg": "????????? ??? ??????????????????"}, status=403)
        try:
            post = Post.objects.get(id=data["id"])
            if request.user in post.likeUsers.all():
                post.likeUsers.remove(request.user)
                serializer_post = PostSerializer(post, context={"request": request})
                return JsonResponse({"data": serializer_post.data, "ok": "????????? ??????"}, status=200)
            else:
                post.likeUsers.add(request.user)
                serializer_post = PostSerializer(post, context={"request": request})
                return JsonResponse({"data": serializer_post.data, "ok": "????????? ??????"}, status=201)
        except ObjectDoesNotExist:
            # except Post.DoesNotExist:
            # ??? ?????? ????????????
            return JsonResponse({"msg": "???????????? ????????????????????????"}, status=404)

    @action(detail=False, methods=["get"])
    def likePost(self, request, likeUsers_id=None):

        # ???????????? ?????????
        # post = Post.objects.get(request.user in User)
        # print(post[0]["like_post_users"])
        posts_list = Post.objects.filter(likeUsers=request.user)
        serializer_post = PostSerializer(posts_list, many=True, context={"request": request})
        return JsonResponse({"data": serializer_post.data, "ok": "?????? ???????????? ?????????"}, status=201)

    # @action(detail=False)
    # def public_list(self, request):
    #     qs = self.queryset.filter(is_public=True)
    #     serializer = self.get_serializer(qs, many=True)
    #     return Response(serializer.data)


class FollowPostView(APIView):
    def get(self, request):
        me = request.user  # ???
        user_list = me.followUser.all()
        posts = []
        for follower in user_list:
            posts_list = Post.objects.filter(user=follower)
            for post in posts_list:
                posts.append(post)
        serializer = FollowerPostSerializer(posts, many=True)
        return JsonResponse({"data": serializer.data, "??????": len(posts), "ok": "?????? ???????????? ????????? ?????????"}, status=201)


class MyPostView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.user.is_anonymous:
            return JsonResponse({"msg": "????????? ??? ??????????????????"}, status=403)
        get_data = request.data  # or request.GET check both
        # posts_list = (Post.objects.filter(user__id=get_data['id']))
        # posts_list = posts.filter(user__id=request.data["id"])
        # posts_list = Post.objects.filter(user__id=request.session.get("_auth_user_id"))
        posts_list = Post.objects.filter(user=request.user)
        serialized_posts = PostSerializer(posts_list, many=True, context={"request": request})
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

        # return JsonResponse({'ok': True, 'status': 200, 'msg': '????????????.'}, status=200)

    # def get(self, request):
    # posts = Post.objects.all()
    # data = posts.filter(user__id=request.session.get("_auth_user_id"))
    # serializer = PostSerializer(data=data)
    # print(data)
    # if serializer.is_valid():
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
