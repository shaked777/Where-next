from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('preference/', views.update_preference, name='update_preference'),
    path('hotels/<str:c_code>/', views.hotels, name='hotels'),
    path('recommend/', views.recommend, name='recommend'),
]