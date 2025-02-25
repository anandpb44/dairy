"""data_manage URL Configuration

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.register),
    path('',views.user_login),
    path('logout',views.user_logout),
    path('home',views.home),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('add_doc',views.add_doc),
    path('add_img',views.add_img),
    path('add_mes',views.add_message),
    path('documents/', views.document_list, name='document_list'),
    path('images/', views.image_list, name='image_list'),
    path('messages/', views.message_list, name='message_list'),
    path('mess_delete/<mid>',views.mess_delete),
]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)