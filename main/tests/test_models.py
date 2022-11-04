from django.test import TestCase
from ..models import Traveler, Preference, Trip
from django.contrib.auth.models import User, Group
from datetime import date
from django.db.utils import DataError

class TestTraveler(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        '''DATA'''
        Group.objects.create(name='traveler')
        User.objects.create(username='test', password='!1234')

    def setUp(self):
        '''set up atr'''
        self.user = User.objects.get(username='test')
        self.traveler = Traveler.objects.get(user_id=self.user.id)

    def test_preference_creation(self):

        Preference.objects.create(traveler=self.traveler, depart_date=date.today()
                                    ,return_date=date(2022,12,12), budget='limitless', point_of_interest='clubs,food', on_season=False)

        self.assertEqual(Preference.objects.get(traveler=self.traveler).depart_date, date.today())

    def test_bad_preference_creation(self):

        self.assertRaises(ValueError, Preference.objects.create,traveler=1, depart_date=date.today()
                            ,return_date=date(2022,10,12), budget='limitless', point_of_interest='clubs,food', on_season=False)

    def test_trip_creation(self):

        Trip.objects.create(name='tel aviv', country='IL', city_code='TLV', info='the white city')
                                    
        self.assertEqual(Trip.objects.get(city_code='TLV').country, 'IL')

    def test_bad_trip_creation(self):

        self.assertRaises(DataError, Trip.objects.create, name='tel aviv', country='ISLL', city_code='TLV', info='the white city')