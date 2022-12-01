"""webAppGenics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app1 import views
urlpatterns = [
    # Here we are assigning the path of our url
    path('', views.signIn),
    path('postsignIn/', views.postsignIn),
    path('signUp/', views.signUp, name="signup"),
    path('logout/',views.logout, name="log"),
    path('postsignUp/', views.postsignUp),  
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contacts, name="contacts"),
    path("loadform/",views.loadform,name="loadform"),
    path("upload/",views.upload,name="upload"),
    path("selection/",views.selection,name="select_user"),
    path("selection/processFile/",views.algorithm,name="algorithm"),
    path("downloadExpert/",views.downloadExpert,name="downloadExpert"), 
    path("downloadRes/",views.downloadRes,name="downloadRes"),
]
