import json

from service.models import User
from rest_framework.viewsets import ModelViewSet
from service.serializers import UserSerializer, UserProfileSerializer, BasicUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignUpView(APIView):
    def post(self, request):
        print("123")
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


class UserLoginView(APIView):
    # 아래 내용 검색해보기
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        input_data = json.loads(request.body)
        user = User.objects.filter(email=input_data['email']).first()

        if not user:
            return JsonResponse(data={
                'ok': False,
                'status': 403,
                'msg': '존재하지 않는 아이디입니다.'
            }, status=403)
        elif not user.check_password(input_data['password']):
            return JsonResponse(data={
                'ok': False,
                'status': 403,
                'msg': '올바른 비밀번호를 입력해주세요.'
            }, status=403)
        login(request, user)
        serializer = UserProfileSerializer(context={'request': request}, instance=user)
        return JsonResponse({'user': serializer.data}, status=201)


class Logout(APIView):
    def get(self, request, format=None):
        # using Django logout
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):
    def get(self, request, format=None):
        if request.user.is_anonymous:
            return JsonResponse({"msg": "로그인 후 이용바랍니다"}, status=403)

        print(request.user)
        user = User.objects.filter(id=request.session.get("_auth_user_id")).first()
        serializer = UserProfileSerializer(context={'request': request}, instance=user)
        return JsonResponse({'user': serializer.data}, status=200)


# FindUserById
class UserSearchId(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.filter(username=data["username"], email=data["email"]).first()
        if user is None:
            return JsonResponse({'msg': "아이디를 찾을 수 없다"}, status=401)

        serializer_user = BasicUserSerializer(user)
        return JsonResponse({'userEmail': serializer_user.data["email"]}, status=200)


class ResetUserPassword(APIView):
    def post(self, request):
        data = request.data

        user = User.objects.filter(id=data['id']).first()
        if not user:
            return JsonResponse({'msg': '에러'})

        else:
            user.set_password(data['newpassword'])
            user.save()
            serializer_user = BasicUserSerializer(user).data
            return Response(serializer_user, status=status.HTTP_200_OK)

        # user = User.objects.get(id=data['id'])
        # serializer = BasicUserSerializer(instance=user)
        #
        # if serializer.is_valid(raise_exception=True):
        #     return Response({'msg': serializer.data}, status=403)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     serializer_user = BasicUserSerializer(user).data
        #     return JsonResponse({'userEmail': serializer_user}, status=200)
        # except:
        #     return JsonResponse({'msg': "에러"}, status=401)


# if serializer.is_valid(raise_exception=True):
#          new_user = serializer.save()
#          if 'password' in data:
#              new_user.set_password(data['password'])
#          else:
#              return Response({'msg': 'password not exist'}, status=403)
#          new_user.save()
#          return Response(UserSerializer(new_user).data)
#      else:
#          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )

class FollowUserView(APIView):
    def post(self, request):
        data = request.data
        if request.user.is_anonymous:
            return JsonResponse({"msg": "로그인 후 이용바랍니다"}, status=403)

        try:
            me = request.user  # 나
            targetUser = User.objects.get(id=data["id"])  # 대상
            if targetUser == me:
                return JsonResponse({"msg": "자기 자신은 팔로우 할 수없습니다"}, status=403)

            if targetUser in me.followUser.all():
                me.followUser.remove(targetUser)
                serializer_user = UserSerializer(me, context={"request": request})
                return JsonResponse({"data": serializer_user.data, "ok": "팔로우 삭제"}, status=200)
            else:
                me.followUser.add(targetUser)
                serializer_user = UserSerializer(me, context={"request": request})
                return JsonResponse({"data": serializer_user.data, "ok": "팔로우 성공"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"msg": "데이터가 존재하지않습니다"}, status=404)
