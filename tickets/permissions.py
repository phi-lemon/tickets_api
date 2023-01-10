from rest_framework import permissions
from .models import Project, Contributor


class IsAuthorOrContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(user=request.user, project=obj).exists() or obj.author == request.user

