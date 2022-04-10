from django.urls import path, include
from django.conf.urls.static import static
from service.views import v1
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', v1.UserViewSet)
router.register('posts', v1.PostViewSet)
router.register('comments', v1.CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("signUp", v1.UserSignUpView.as_view()),
    path("signIn", v1.UserLoginView.as_view()),
    path("logout", v1.Logout.as_view()),
    path("myPost", v1.MyPostView.as_view()),
    path("profile", v1.UserProfile.as_view()),
    path("searchId", v1.UserSearchId.as_view()),
    path("resetPassword",v1.ResetUserPassword().as_view()),
    path("follow", v1.FollowUserView.as_view()),
    path("followPost", v1.FollowPostView.as_view())
    # path("users", v1.UserViewSet)
]
