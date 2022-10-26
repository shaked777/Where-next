from django.core.management.base import BaseCommand
import pandas as pd
from main.models import Trip



class Command(BaseCommand):

    def handle(self, *args, **options):

        # Process data with Pandas
        data = pd.read_csv("/Users/shakedgabay/Desktop/python/python_course/reccomandition_system/world_cities.csv")
        data = data.rename(columns={'description ': 'description'})

        # iterate over DataFrame and create your objects
        for trip in data.itertuples():
            Trip.objects.create(country=trip.iso2, city_code=trip.city_code, info=trip.description)
