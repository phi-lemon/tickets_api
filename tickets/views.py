from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from .serializers import UserSignupSerializer
from .models import Project, Contributor
from accounts.models import CustomUser

from .permissions import IsAuthorOrContributor
from .serializers import ProjectSerializer, UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrContributor,)

    def get_queryset(self):
        """
        List projects where authenticated user is author or contributor
        """
        user = self.request.user
        query_contributor = user.contributor.all()
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__in=query_contributor)
        return projects.distinct()

    serializer_class = ProjectSerializer


class UserViewSet(viewsets.ModelViewSet):
    # todo ajouter author
    queryset = Contributor.objects.all().select_related('project')

    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        project = Project.objects.get(id=project_id)
        return self.queryset.filter(project=project)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer


# class ProjectList(generics.ListCreateAPIView):
#     permission_classes = (IsAuthorOrContributor,)
#
#     def get_queryset(self):
#         """
#         List projects where authenticated user is author or contributor
#         """
#         user = self.request.user
#         query_contributor = user.contributor.all()
#         projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__in=query_contributor)
#         return projects.distinct()
#
#     serializer_class = ProjectSerializer
#
#
# class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthorOrContributor,)
#
#     def get_queryset(self):
#         """
#         List projects where authenticated user is author or contributor
#         """
#         user = self.request.user
#         query_contributor = user.contributor.all()
#         projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__in=query_contributor)
#         return projects.distinct()
#
#     serializer_class = ProjectSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthorOrContributor,)
#
#     def get_queryset(self):
#         """
#         List users
#         """
#         contributors = Contributor.objects.all()
#         return contributors
#
#     serializer_class = UserSerializer


