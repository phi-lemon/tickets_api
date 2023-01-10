from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from .serializers import UserSignupSerializer
from .models import Project
from .permissions import IsAuthorOrContributor
from .serializers import ProjectSerializer


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


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
