from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .permissions import IsAuthenticated, IsAuthorOrReadOnly, IsProjectAuthorOrContributorReadOnly, \
    IsIssueCommentContributor
from .serializers import UserSignupSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, \
    CommentSerializer
from .models import Project, Contributor, Issue, Comment


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        List projects where authenticated user is author or contributor
        """
        user = self.request.user
        query_contributor = user.contributor.all()
        projects = Project.objects.filter(contributor__in=query_contributor)
        return projects.distinct()

    def perform_create(self, serializer):
        """
        setting implicite attributes
        """
        author = self.request.user
        serializer.save(author=author)


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsIssueCommentContributor)
    serializer_class = IssueSerializer

    def get_queryset(self):
        """
        List project's issues
        """
        issues = Issue.objects.filter(project=self.kwargs['project_pk'])
        return issues

    def perform_create(self, serializer):
        """
        setting implicite attributes
        """
        author = self.request.user
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(author=author, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsIssueCommentContributor)
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        List issue's comments
        """
        comments = Comment.objects.filter(issue=self.kwargs['issue_pk'])
        return comments

    def perform_create(self, serializer):
        """
        setting implicite attributes
        """
        user = self.request.user
        issue = Issue.objects.get(id=self.kwargs['issue_pk'])
        serializer.save(user=user, issue=issue)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsProjectAuthorOrContributorReadOnly)
    serializer_class = ContributorSerializer

    def get_queryset(self, *args, **kwargs):
        """
        List project's contributors
        """
        contributors = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        return contributors

    def perform_create(self, serializer):
        """
        setting implicite attributes
        """
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(project=project)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
