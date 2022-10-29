from django.db import models
from django import forms
from accounts.models import Traveler
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField

# Create your models here.

class Preference(models.Model):

    POINT_OF_INTERESTS = [   

    ('food', ' Food'),
    ('history', ' History'),
    ('sport', ' Sport'),
    ('clubs', ' Night life'),
    ('shopping', ' Shopping'),
    ]

    BUDGET = [   
    ('limitless', ' No limit'),
    ('budget', ' On a budget'),
    ('regular', ' Regular'),
    ]

    traveler = models.OneToOneField(Traveler, on_delete=models.CASCADE, related_name='preference')
    depart_date = models.DateField()
    return_date = models.DateField()
    budget = models.CharField(max_length=50, choices=BUDGET, default='regular')
    point_of_interest = MultiSelectField(choices=POINT_OF_INTERESTS)
    on_season = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.traveler.user.username} preferences"

class PreferenceForm(forms.ModelForm):
    
    class Meta:
        model = Preference
        fields = '__all__'
        exclude = ['traveler']
        widgets = {
        'depart_date': forms.SelectDateWidget(),
        'return_date': forms.SelectDateWidget(),
        'point_of_interest':  forms.CheckboxSelectMultiple()
        } 

class Trips(models.Model):

    POINT_OF_INTERESTS = [   
    ('food', ' Food'),
    ('history', ' History'),
    ('sport', ' Sport'),
    ('clubs', ' Night life'),
    ('shopping', ' Shopping'),
    ]

    country = CountryField()
    city_code = models.CharField(max_length=5, default='0')
    season_start = models.DateField()
    season_end = models.DateField()
    famous_for = MultiSelectField(choices=POINT_OF_INTERESTS)
    info = models.CharField(max_length=256)

    def __str__(self):
        return f"trip to: {self.country.name}"

class Trip(models.Model):

    name = models.CharField(max_length=15, default='-')
    country = CountryField()
    city_code = models.CharField(max_length=5, default='0')
    info = models.TextField()

    def __str__(self):
        return f"trip to: {self.country.name}"