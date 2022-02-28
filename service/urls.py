from django.urls import path, include
from django.conf.urls.static import static
from service.views import v1
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', v1.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("users", v1.UserViewSet)
]
