from django.urls import path
from .views import ProjectList, ProjectDetail, RegisterView

urlpatterns = [
    path("projects/<int:pk>/", ProjectDetail.as_view(), name="project_detail"),
    path("projects/", ProjectList.as_view(), name="project_list"),
    path('signup/', RegisterView.as_view(), name="sign_up"),
]
