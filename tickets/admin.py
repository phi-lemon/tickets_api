from django.contrib import admin

from .models import Project, Contributor, Issue, Comment


admin_models = [Issue, Comment]
admin.site.register(admin_models)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
