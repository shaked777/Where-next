from django.db import models
from django.contrib.auth.models import User
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# Create your models here.

class Traveler(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='traveler')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    country = CountryField()
    avatar_img = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class TravelerForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = '__all__'
        exclude = ['user']
        widgets = {'country': CountrySelectWidget()}
