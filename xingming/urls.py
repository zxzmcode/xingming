"""xingming URL Configuration

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
from django.urls import path, include

from article.views import index_view, about_author

extra_patterns = [

]

urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置主页入口
    path('', index_view),
    # 配置about的入口
    path('about/', about_author, name='about'),
    # 配置article的入口
    path('article/', include('article.urls', namespace='article')),
]
