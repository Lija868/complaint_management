from django.db import models
from django.utils import timezone

from users.models import APIUser
from .constants import TASK_STATUS, PRIORITY


class Task(models.Model):
    task_id = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True,)
    status = models.CharField(max_length=100, choices=TASK_STATUS, default='TODO')
    assignee = models.ForeignKey(
        APIUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE, related_name="assignee")
    created_by = models.ForeignKey(
        APIUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="created_by",
    )
    estimate = models.CharField(max_length=300, null=True, blank=True)
    start_date = models.DateField(null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)
    priority = models.CharField(max_length=100, choices=PRIORITY, null=True)
    attachment = models.FileField(null=True,blank=True, upload_to='tasks/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

