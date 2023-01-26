from django.urls import path, re_path
from .views import ProjectViewSet, UserViewSet, IssueViewSet, CommentViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
    # Contributors
    re_path(r'^projects/(?P<project_pk>\d+)/users/?$', UserViewSet.as_view({'get': 'list', 'post': 'create'}),
            name="project_users_list_post"),
    re_path(r'^projects/(?P<project_pk>\d+)/users/(?P<pk>\d+)/?$',
            UserViewSet.as_view({'delete': 'destroy'}), name="project_users_delete"),
    # Issues
    re_path(r'^projects/(?P<project_pk>\d+)/issues/?$',
            IssueViewSet.as_view({'get': 'list', 'post': 'create'}),
            name="issues_list_post"),
    re_path(r'^projects/(?P<project_pk>\d+)/issues/(?P<pk>\d+)/?$',
            IssueViewSet.as_view({'put': 'update', 'delete': 'destroy'}),
            name="issue_detail"),
    # Comments
    re_path(r'^projects/(?P<project_pk>\d+)/issues/(?P<issue_pk>\d+)/comments/?$',
            CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
            name="comments_list_post"),
    re_path(r'^projects/(?P<project_pk>\d+)/issues/(?P<issue_pk>\d+)/comments/(?P<pk>\d+)/?$',
            CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
            name="comment_detail"),
]

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns += router.urls
