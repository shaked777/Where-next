from django.urls import path
from . import views

urlpatterns = [
    path('singup/', views.sing_up, name='sing_up'),
    path('singin/', views.sing_in, name='sing_in'),
    path('singout/', views.user_logout, name='sing_out'),
    path('update/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    

]