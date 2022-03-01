from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, room):
        return room.user == request.user
        # 결과값은 트루 폴스다 room이 obj여서 has_object_permission
