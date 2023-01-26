from django.contrib import admin

from .models import Project, Contributor, Issue, Comment


class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    inlines = (ContributorInline,)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'author', 'assignee')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment)

