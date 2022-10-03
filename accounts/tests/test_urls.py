from django.test import TestCase
from .. import views
from django.urls import reverse, resolve


class TestUrls(TestCase):
    
    def test_urls_resolve(self):
        profile_url = reverse('profile')
        self.assertEquals(resolve(profile_url).func, views.profile)
        
        update_url = reverse('update_profile')
        self.assertEquals(resolve(update_url).func, views.update_profile)