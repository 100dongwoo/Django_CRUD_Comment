from django.urls import path, include
from django.conf.urls.static import static
from service.views import v1
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', v1.UserViewSet)
router.register('posts', v1.PostViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("signUp", v1.UserSignUpView.as_view()),
    path("signIn", v1.UserLoginView.as_view()),
    path("logout", v1.Logout.as_view()),
    path("myPost",v1.MyPostView.as_view())
    # path("users", v1.UserViewSet)
]
