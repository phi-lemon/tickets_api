from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)

    # types
    BACKEND = 'B'
    FRONTEND = 'F'
    IOS = 'I'
    ANDROID = 'A'
    TYPE_CHOICES = [
        (BACKEND, 'Backend'),
        (FRONTEND, 'Frontend'),
        (IOS, 'Ios'),
        (ANDROID, 'Android'),
    ]
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=None,
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='contributors')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contributor', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

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
        default=CONTRIBUTOR,
    )

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return str(self.user) + " - " + str(self.project)


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048)
    # tag
    BUG = 'B'
    EVOLUTION = 'E'
    TASK = 'T'
    TAG_CHOICES = [
        (BUG, 'Bug'),
        (EVOLUTION, 'Evolution'),
        (TASK, 'Task'),
    ]
    tag = models.CharField(
        max_length=1,
        choices=TAG_CHOICES,
        default=TASK,
    )
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
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    # status
    TODO = 'T'
    IN_PROGRESS = 'I'
    CLOSED = 'C'
    STATUS_CHOICES = [
        (TODO, 'Todo'),
        (IN_PROGRESS, 'In progress'),
        (CLOSED, 'Closed'),
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=TODO,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_author',
                               on_delete=models.SET(get_sentinel_user))
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_assignee',
                                 on_delete=models.SET(get_sentinel_user))
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=2048)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_author', on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
