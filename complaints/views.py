
# Create your views here.
import hashlib
import random
import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from authentication.authentication import JwtTokensAuthentication
from complaint_management.settings import logger
from complaints.models import Task
from complaints.serializers import TaskSerializer
from utils.message_utils import get_message
from utils.pagination import CustomPageNumberPagination


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination
    authentication_classes = [
        JwtTokensAuthentication, SessionAuthentication, BasicAuthentication
    ]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_queryset(self):
        assignee = self.request.query_params.get("assignee")
        queryset = Task.objects.all().order_by("-created_at")

        if assignee:
            queryset = queryset.filter(assignee=assignee)

        return queryset

    def create(self, request, *args, **kwargs):
        user_id = request.user.get("user_id")
        data = request.data
        data["created_by"] = user_id
        task_id = hashlib.md5(request.get("title").encode() + (str(time)).encode()).hexdigest()

        data["task_id"] = task_id
        try:
            user_obj = get_user_model().objects.get(id=user_id, is_verified=True)
        except ObjectDoesNotExist:
            return Response(
                {"code": 204, "message": get_message(204)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            serializer = TaskSerializer(data)
            if serializer.is_valid():
                serializer.save()
                return Response({"code": 200, "message": get_message(200)})
            else:
                return Response(
                    {"code": 400, "message": get_message(400),
                     "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.error(e)
            print(e)
            return Response(
                {"code": 114, "message": get_message(114)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk", None)
        user_id = request.user.get("user_id")
        description = request.data.get("description", None)
        assignee = request.data.get("assignee", None)
        title = request.data.get("title", None)
        try:
            get_user_model().objects.get(id=user_id, is_verified=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            return Response(
                {"code": 204, "message": get_message(204)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            task = Task.objects.get(pk=pk, created_by=user_id)
            task.description = description
            task.assignee_id = assignee
            task.title = title
            task.updated_at = timezone.now()
            task.save()
            return Response({"code": 200, "message": get_message(200)})
        except Exception as ex:
            logger.error(ex)
            return Response(
                {"code": 114, "message": get_message(114)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.get("user_id")
        try:
            get_user_model().objects.get(id=user_id, is_verified=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            return Response(
                {"code": 204, "message": get_message(204)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            Task.objects.get(pk=kwargs["pk"], created_by=user_id).delete()
            # super().destroy(request)
            return Response(
                {
                    "code": 200,
                    "message": get_message(200),
                }
            )

        except Exception:
            return Response(
                {"code": 114, "message": get_message(114)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
