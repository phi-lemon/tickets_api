from django.urls import path, re_path
# from .views import UserViewSet
from .views import ProjectViewSet, UserViewSet
from rest_framework.routers import SimpleRouter


urlpatterns = [
    re_path(r'^projects/(?P<project_pk>\d+)/users/?$', UserViewSet.as_view({'get': 'list', 'post': 'create'}),
            name="project_users_list_post"),
]

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns += router.urls

