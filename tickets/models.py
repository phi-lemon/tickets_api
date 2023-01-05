from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Project(models.Model):
    project_id = models.IntegerField
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=128)
    contributor_user_id = models.ForeignKey('Contributor', on_delete=models.PROTECT)


class Contributor(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    project_id = models.ForeignKey(Project, on_delete=models.PROTECT)

    # permissions
    READ = 'R'
    WRITE = 'W'
    PERMISSION_CHOICES = [
        (READ, 'ReadOnly'),
        (WRITE, 'Edit'),
    ]
    permission = models.CharField(
        max_length=1,
        choices=PERMISSION_CHOICES,
        default=READ,
    )

    # roles
    AUTHOR = 'A'
    CONTRIBUTOR = 'C'
    ROLE_CHOICES = [
        (AUTHOR, 'Author'),
        (CONTRIBUTOR, 'Contributor'),
    ]
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default=READ,
    )


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=50)
    # priority
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    # status
    OPEN = 'O'
    CLOSED = 'C'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    author_user_id = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='author',
                                          on_delete=models.SET(get_sentinel_user))
    assignee_user_id = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='assignee',
                                            on_delete=models.SET(get_sentinel_user))
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
