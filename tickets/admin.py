from django.contrib import admin

from .models import Project, Contributor, Issue, Comment


admin_models = [Project, Issue, Comment]
admin.site.register(admin_models)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


admin.site.register(Contributor, ContributorAdmin)
