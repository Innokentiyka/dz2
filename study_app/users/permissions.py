from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsOwnerOrStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner
