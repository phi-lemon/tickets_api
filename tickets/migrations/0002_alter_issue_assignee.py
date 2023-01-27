# Generated by Django 4.0.8 on 2023-01-27 08:39

from django.conf import settings
from django.db import migrations, models
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(tickets.models.get_sentinel_user), related_name='issue_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
