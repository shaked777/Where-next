from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse

class TestView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        '''DATA'''
        Group.objects.create(name='traveler')
        User.objects.create(username='test', password='!1234')

    def setUp(self) -> None:
        self.user = User.objects.get(username='test')
        self.client = Client()
        self.sing_up_url = reverse('sign_up')
        self.sing_in_url = reverse('sign_in')
        self.sing_out_url = reverse('sign_out')
        self.profile_url = reverse('profile')
        self.update_profile_url = reverse('update_profile')

    def test_sing_up_GET(self):
        response = self.client.get(self.sing_up_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign-up.html')

    def test_sing_in_GET(self):
        response = self.client.get(self.sing_in_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign-in.html')

        self.client.force_login(self.user)

        response = self.client.get(self.sing_in_url)
        self.assertRedirects(response, '/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        
    def test_sing_out_GET(self):
        response = self.client.get(self.sing_out_url)

        self.assertEqual(response.status_code, 302)

    def test_update_preference_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(self.update_profile_url, {'user':self.user.id, 'first_name':'test', 'last_name':'test', 'email':'test@gmail.com', 'country':'US'})
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.traveler.email, 'test@gmail.com')

    def test_profile_GET(self):
        '''not logged in'''
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        '''logged in'''
        self.client.force_login(self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')