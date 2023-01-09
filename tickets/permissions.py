from rest_framework import permissions
from .models import Project, Contributor


class IsContributor(permissions.BasePermission):
    # def has_permission(self, request, view):
        # Authenticated users only can see list view
        # if request.user.is_authenticated:
        #     return True
        # return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # Write permissions are only allowed to the author of a project
        return obj.author == request.user  # todo ou contributeur

