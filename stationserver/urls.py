"""stationserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from serverapp import views
from django.conf.urls import url


app_name ='serverapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    url(r'^serial$', views.serial, name='serial'),
    path('recvdata1/', views.recvdata1),
    path('select1/', views.select1, name='select1'),
    path('show1/', views.show1, name='show1'),
    path('newest1/', views.newest1, name='newest1'),
    path('process/', views.process, name='process'),
    url(r'^search1$', views.search1,name='search1'),
    path('recvdata2/', views.recvdata2),
    path('select2/', views.select2, name='select2'),
    path('show2/', views.show2, name='show2'),
    path('newest2/', views.newest2, name='newest2'),
    url(r'^search2$', views.search2,name='search2'),
]
