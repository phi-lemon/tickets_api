from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from accounts.models import CustomUser
from .serializers import UserSignupSerializer, ProjectSerializer, UsersListSerializer, UsersCreateSerializer
from .models import Project, Contributor
from .permissions import IsAuthorOrReadOnly, IsProjectContributorOrAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        """
        List projects where authenticated user is author or contributor
        """
        user = self.request.user
        query_contributor = user.contributor.all()
        projects = Project.objects.filter(contributor__in=query_contributor)
        return projects.distinct()

    serializer_class = ProjectSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectContributorOrAuthor,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsersListSerializer
        if self.request.method == 'POST':
            return UsersCreateSerializer

    def get_queryset(self, *args, **kwargs):
        self.queryset = Contributor.objects.all().select_related('project')
        project = Project.objects.get(id=self.kwargs.get("project_pk"))
        print(self.queryset.filter(project=project, user=4))
        return self.queryset.filter(project=project)

    def create(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=request.data['user'])
        contributor = Contributor.objects.create(user=user, project_id=kwargs['project_pk'])
        contributor.save()
        return Response(status=201)

    def destroy(self, request, *args, **kwargs):
        contributor = Contributor.objects.get(project_id=kwargs['project_pk'], user_id=kwargs['pk'])
        self.perform_destroy(contributor)
        return Response(status=204)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
