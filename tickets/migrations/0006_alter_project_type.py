# Generated by Django 4.0.8 on 2023-01-27 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_alter_issue_assignee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('B', 'Backend'), ('F', 'Frontend'), ('I', 'Ios'), ('A', 'Android')], default=None, max_length=1, null=True),
        ),
    ]
