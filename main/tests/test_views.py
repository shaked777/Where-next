from django.forms import ValidationError
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ..models import Trip, Traveler, Preference
from datetime import date
from django.core.exceptions import ValidationError
from django.urls import reverse

class TestView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        '''DATA'''
        Group.objects.create(name='traveler')
        User.objects.create(username='test', password='!1234')
        Trip.objects.create(name='Tel aviv', country='IL', city_code='TLV', info='the white city')
        Trip.objects.create(name='Test', country='IL', city_code='Test', info='food')
        Preference.objects.create(traveler=User.objects.get(username='test').traveler, depart_date=date.today()
                                    ,return_date=date(2022,12,12), point_of_interest='clubs,food', on_season=False)

    def setUp(self) -> None:
        self.user = User.objects.get(username='test')
        self.traveler = Traveler.objects.get(user_id=self.user.id)
        self.client = Client()
        self.update_preference_url = reverse('update_preference')
        self.hotels_url = reverse('hotels', kwargs={'c_code':'TLV'})
        self.recommender_url = reverse('recommender') 

    def test_preference_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.update_preference_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/update_preference.html')

    def test_preference_POST(self):
        self.client.force_login(self.user)
        
        response = self.client.post(self.update_preference_url, {'traveler':self.traveler, 'depart_date':date.today()
                                ,'return_date':date(2022,12,12), 'budget':'limitless', 'point_of_interest':['clubs','food'], 'on_season':False})
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.traveler.preference.budget, 'limitless')

    def test_bad_preference_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(self.update_preference_url, {'traveler':self.traveler, 'depart_date':date.today()
                            ,'return_date':date(2022,10,12), 'budget':'limitless', 'point_of_interest':['clubs','food'], 'on_season':False})
        
        self.assertNotEqual(self.traveler.preference.return_date, date(2022,10,12))

    def test_hotels_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.hotels_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/hotels.html')

    def test_recommend_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.recommender_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/recommend.html')