from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserSignupSerializer
from .models import Project
from .permissions import IsContributor
from .serializers import ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsContributor,)

    def get_queryset(self):
        """
        List projects where authenticated user is author or contributor
        :return:
        """
        user = self.request.user
        projects = Project.objects.filter(contributor__user_id=user.id) | Project.objects.filter(author=user)
        return projects.distinct()

    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsContributor,)

    queryset = Project.objects.all()

    # def get_queryset(self):
    #     """
    #     List projects where authenticated user is author or contributor
    #     :return:
    #     """
    #     user = self.request.user
    #     projects = Project.objects.filter(contributor__user_id=user.id) | Project.objects.filter(author=user)
    #     return projects.distinct()

    serializer_class = ProjectSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
