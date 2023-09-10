from rest_framework.permissions import BasePermission


class IsAdminAK(BasePermission):

    def has_permission(self, request, view):
        return bool('adminAK' in [g.name for g in request.user.groups.all()])


class IsVerifikator(BasePermission):

    def has_permission(self, request, view):
        return bool('verifikator' in [g.name for g in request.user.groups.all()])
