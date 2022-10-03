from django.test import TestCase
from ..models import Traveler
from django.contrib.auth.models import User, Group

class TestTraveler(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        '''DATA'''
        Group.objects.create(name='traveler')
        User.objects.create(username='test', password='!1234')

    def setUp(self):
        '''set up atr'''
        self.user = User.objects.get(username='test')

    def test_traveler_creation(self):
        
        traveler = Traveler.objects.get(user_id=self.user.id)
        self.assertTrue(isinstance(traveler, Traveler))
        self.assertEqual(traveler.user_id, self.user.id)
        self.assertTrue(traveler.avatar_img == 'default.png')
