"""the_career_mentor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .views import RegisterAPI, LoginAPI
from django.urls import path
from knox import views as knox_views
from django.urls import path
from . import views
#from .views import RegisterAPI
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.fun1, name='home page'), # Add this line
    path('Form/', views.fun2, name='Form page'), # Add this line
    path('About/', views.fun3, name='About page'), # Add this line
    path('Blogs/', views.fun4, name='Blogs page'), # Add this line
    path('Login/', views.fun5, name='Login page'), # Add this line
    path('Register/', views.fun6, name='Register page'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'), # Add this line
]
