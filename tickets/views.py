from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .permissions import IsAuthorOrReadOnly, IsProjectContributorOrAuthor
from .serializers import UserSignupSerializer, ProjectSerializer, ContributorCreateSerializer, ContributorListSerializer
from .models import Project, Contributor


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        List projects where authenticated user is author or contributor
        """
        user = self.request.user
        query_contributor = user.contributor.all()
        projects = Project.objects.filter(contributor__in=query_contributor)
        return projects.distinct()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectContributorOrAuthor,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContributorListSerializer
        if self.request.method == 'POST':
            return ContributorCreateSerializer

    def get_queryset(self, *args, **kwargs):
        contributors = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        return contributors


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
