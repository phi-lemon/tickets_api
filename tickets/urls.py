from django.urls import path, re_path
from .views import ProjectViewSet, UserViewSet
# from rest_framework.routers import SimpleRouter
# from .views import ProjectList, ProjectDetail

# standard views urls patterns
# urlpatterns = [
#     path("projects/<int:pk>/", ProjectDetail.as_view(), name="project_detail"),
#     path("projects/", ProjectList.as_view(), name="project_list"),
# ]


urlpatterns = [
    path("projects/<int:pk>/", ProjectViewSet.as_view({'get': 'retrieve'}), name="project_detail"),
    path("projects/", ProjectViewSet.as_view({'get': 'list'}), name="project_list"),
    re_path(r'^projects/(?P<project_pk>\d+)/users/?$', UserViewSet.as_view({'get': 'list'}),
            name="project_users_list"),
]

# router = SimpleRouter()
# router.register("projects", ProjectViewSet, basename="projects")
# router.register("users", UserViewSet, basename="users")
#
# urlpatterns = router.urls
