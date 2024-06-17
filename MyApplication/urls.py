"""
URL configuration for MyApplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', home.index, name='index'),
    path("login/", home.login, name="login"),
    path("register/", home.register, name="register"),
    path("user_register/", home.user_register, name="user_register"),
    path("user_login/", home.user_login, name="user_login"),
    path("PasswordManage/", include("PasswordManageSystem.urls")),
    path("LedgerManage/", include("LedgerManageSystem.urls")),
    path("PersonManage/", include("PersonManageSystem.urls")),
    path("CookbookManage/", include("CookbookManageSystem.urls")),
]