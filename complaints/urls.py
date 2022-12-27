
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from complaints.views import TaskViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"task", TaskViewSet, basename="Task")

urlpatterns = [
    path(r"", include(router.urls)),
]
