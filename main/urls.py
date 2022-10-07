from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('preference', views.update_preference, name='update_preference'),
]