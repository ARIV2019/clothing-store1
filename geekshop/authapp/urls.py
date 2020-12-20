from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    #re_path(r'^login/$', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    #re_path(r'^logout/$', authapp.logout, name='login'),
    path('register/', authapp.register, name='register'),
    #re_path(r'^register/$', authapp.register, name='login'),
    path('edit/', authapp.edit, name='edit'),
    #re_path(r'^edit/$', authapp.edit, name='login'),
    #path('verify/<email>/<activation_key>/', authapp.verify, name='verify')
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
]

