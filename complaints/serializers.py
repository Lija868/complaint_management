# -*- coding: utf-8 -*-
from rest_framework import serializers

from complaints.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ["created_at", "updated_at"]
