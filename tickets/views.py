from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .permissions import IsAuthenticated, IsAuthorOrReadOnly, IsProjectAuthorOrContributorReadOnly, \
    IsIssueAuthorOrContributorReadOnly
from .serializers import UserSignupSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer
from .models import Project, Contributor, Issue


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
    permission_classes = (IsAuthenticated, IsIssueAuthorOrContributorReadOnly)
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


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsProjectAuthorOrContributorReadOnly)
    serializer_class = ContributorSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return ContributorListSerializer
    #     else:
    #         return ContributorCreateSerializer

    def get_queryset(self, *args, **kwargs):
        contributors = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        return contributors

    def perform_create(self, serializer):
        """
        setting implicite attributes
        """
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(project=project)


    # def create(self, validated_data):
    #     project = Project.objects.get(id=self.context['view'].kwargs['project_pk'])
    #     contributor = Contributor.objects.create(
    #         user=validated_data["user"],
    #         project_id=project.pk
    #     )
    #     return contributor


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
