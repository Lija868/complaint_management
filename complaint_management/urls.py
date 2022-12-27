"""complaint_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [


    path(
        "openapi",
        get_schema_view(
            title="API",
            description="Internal endpoints to support our  products",
            version="0.0.0",
        ),
        name="openapi-schema",
    ),
    path('docs/', login_required(TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), login_url="/admin"), name='swagger-ui'),

    path('admin/', admin.site.urls),
    path("user/", include("users.urls")),
    path("complaints/", include("complaints.urls")),

]
