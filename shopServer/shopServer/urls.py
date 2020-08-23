"""shopServer URL Configuration

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

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from shopServer import settings
from goods import views as goods
from vips import views as vips
from projs import views as projs
from staffs import views as staffs
from webSource import views as webSource

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webSource.index),
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'^api/goods/(?P<fucname>[a-zA-Z0-9]+)/$', goods.usefucbyname),
    re_path(r'^api/vips/(?P<fucname>[a-zA-Z0-9]+)/$', vips.usefucbyname),
    re_path(r'^api/projs/(?P<fucname>[a-zA-Z0-9]+)/$', projs.usefucbyname),
    re_path(r'^api/staffs/(?P<fucname>[a-zA-Z0-9]+)/$', staffs.usefucbyname),
]
