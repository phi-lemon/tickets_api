from rest_framework import generics
from rest_framework.permissions import AllowAny
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
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
