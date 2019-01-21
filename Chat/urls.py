"""Chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^room/(?P<room_name>\w+)/$', views.room, name='room'),
    re_path(r'^logout/$', views.log_out, name='logout'),
    re_path(r'^login/$', views.log_in, name='login'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^users/change/$', views.personal_area_change, name='personal_area_change'),
    re_path(r'^users/(?P<user_name>.+)/$', views.personal_area, name='personal_area'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
