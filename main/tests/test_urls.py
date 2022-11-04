from django.test import TestCase
from .. import views
from django.urls import reverse, resolve


class TestUrls(TestCase):
    
    def test_hotels_urls_resolve(self):
        hotels_url = reverse('hotels', kwargs={'c_code':'NYC'})
        self.assertEquals(resolve(hotels_url).func, views.hotels)

    def test_update_preference_urls_resolve(self):
        update_url = reverse('update_preference')
        self.assertEquals(resolve(update_url).func, views.update_preference)

    def test_recommender_urls_resolve(self):
        recommender_url = reverse('recommender')
        self.assertEquals(resolve(recommender_url).func, views.recommender)