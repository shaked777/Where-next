from django.core.exceptions import ValidationError
from datetime import date
from django.db import models
from django import forms
from sqlalchemy import null
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
    depart_date = models.DateField(null=False)
    return_date = models.DateField(null=False)
    budget = models.CharField(max_length=50, choices=BUDGET, default='regular', null=False)
    point_of_interest = MultiSelectField(choices=POINT_OF_INTERESTS, min_choices=2, null=False)
    on_season = models.BooleanField(default=False)


    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

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

    def clean(self):
        cleaned_data = super(PreferenceForm, self).clean()
        depart_date = cleaned_data.get("depart_date")
        return_date = cleaned_data.get("return_date")
        poi = cleaned_data.get("point_of_interest")
        if depart_date < date.today() or depart_date >= return_date:
            raise ValidationError("Invalid date")
        elif poi == None or len(poi) < 2:
            raise ValidationError("You need to pick 2 or more Point of interest")
        

class Trip(models.Model):

    name = models.CharField(max_length=15)
    country = CountryField(max_length=2)
    city_code = models.CharField(max_length=5)
    info = models.TextField()

    def __str__(self):
        return f"trip to: {self.country.name}"