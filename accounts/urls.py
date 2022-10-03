from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.sing_up, name='sign_up'),
    path('signin/', views.sing_in, name='sign_in'),
    path('signout/', views.user_logout, name='sign_out'),
    path('update/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    
]