import json

from service.models import User
from rest_framework.viewsets import ModelViewSet
from service.serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout


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
