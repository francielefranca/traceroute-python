from django.urls import path
from . import views

app_name = 'projredesapp'

urlpatterns = [
    path('home', views.home, name='home'),
    path('traceroute/', views.traceroute, name='traceroute'),
]