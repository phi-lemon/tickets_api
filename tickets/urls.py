# from django.urls import path
from rest_framework.routers import SimpleRouter
# from .views import ProjectList, ProjectDetail
from .views import ProjectViewSet

# urlpatterns = [
#     path("projects/<int:pk>/", ProjectDetail.as_view(), name="project_detail"),
#     path("projects/", ProjectList.as_view(), name="project_list"),
# ]

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns = router.urls
