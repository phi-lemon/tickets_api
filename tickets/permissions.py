from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Contributor, Project


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # read permissions
            return True
        return obj.author == request.user


class IsProjectContributorOrAuthor(permissions.BasePermission):

    def has_permission(self, request, view):  # list view
        project = get_object_or_404(Project, pk=view.kwargs["project_pk"])
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return project.contributors.contains(request.user)
        return project.author == request.user  # only author has write permissions

    def has_object_permission(self, request, view, obj):  # list and detail view
        return False  # Not used


class IsContributorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):  # list view
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):  # list and detail view
        if request.method in permissions.SAFE_METHODS:  # read permissions only
            return True
        return Contributor.objects.filter(user=request.user, project=obj).exists()
