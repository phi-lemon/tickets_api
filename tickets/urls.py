from django.urls import path
from .views import ProjectList, ProjectDetail

urlpatterns = [
    path("projects/<int:pk>/", ProjectDetail.as_view(), name="project_detail"),
    path("projects/", ProjectList.as_view(), name="project_list"),
]
