from django.contrib import admin

# Register your models here.
from complaints.models import Task


class TaskAdmin(admin.ModelAdmin):
    """TaskAdmin"""

    list_filter = (
        "assignee",
    )

    list_display = ["task_id", "title", "priority", "assignee", "status", "due_date"]

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context={})

admin.site.register(Task, TaskAdmin)
