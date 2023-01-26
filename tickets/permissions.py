from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Project, Comment, Issue


class IsAuthenticated(permissions.BasePermission):
    """
    Access: user must be authenticated
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Get, post: no restriction
    Update: must be author
    """

    def has_object_permission(self, request, view, obj):
        # not applied when creating objects (post)
        # See https://www.django-rest-framework.org/api-guide/permissions/#limitations-of-object-level-permissions
        if request.method in permissions.SAFE_METHODS:  # read permissions
            return True
        return obj.author == request.user


class IsProjectAuthorOrContributorReadOnly(permissions.BasePermission):
    """
    Access: restricted to contributors
    Post: must be author
    No object permissions needed here
    """

    def has_permission(self, request, view):
        project = get_object_or_404(Project, pk=view.kwargs["project_pk"])
        if request.method in permissions.SAFE_METHODS:
            return project.contributors.contains(request.user)
        return project.author == request.user  # only author has write permissions


class IsIssueCommentContributor(permissions.BasePermission):
    """
    Get, Post: restricted to contributors (author is contributor)
    Update, Delete: must be author or assignee
    """

    def has_permission(self, request, view):
        project = get_object_or_404(Project, pk=view.kwargs["project_pk"])
        return project.contributors.contains(request.user)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Issue):
            return obj.author == request.user or obj.assignee == request.user
        elif isinstance(obj, Comment):
            return obj.user == request.user
