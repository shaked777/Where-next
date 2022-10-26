from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Preference)
admin.site.register(models.Trips)
admin.site.register(models.Trip)