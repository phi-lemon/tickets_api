from rest_framework import generics
from .serializers import UserSignupSerializer

from .models import Project
from .permissions import IsAuthorOrReadOnly
from .serializers import ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
