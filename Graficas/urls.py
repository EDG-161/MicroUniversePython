"""Graficas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import *
from django.urls import path
from EnvGr import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('plot/', views.plot),
    url(r"^plot/(?P<id>[^/]+)/$", views.plot),
    url(r"^grafica/(?P<id>[^/]+)/$", views.data),
    url(r"^graficar/(?P<id>[^/]+)/$", views.dataR),
    url(r"^regG/(?P<h1>[^/]+)/(?P<p1>[^/]+)/(?P<h2>[^/]+)/(?P<p2>[^/]+)/(?P<h3>[^/]+)/(?P<p3>[^/]+)/(?P<id>[^/]+)/$", views.regGrown),
    url(r"^graficart/", views.RG),
    url(r"^gtr/", views.templateGraf),
    url(r"^data/(?P<id>[^/]+)/(?P<t>[^/]+)/$", views.POEA),
    url(r"^dataf/(?P<id>[^/]+)/(?P<t>[^/]+)/$", views.POF),
    url(r"^compararPoblaciones/(?P<id>[^/]+)/$", views.compararPoblaciones),
]
