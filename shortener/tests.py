from django.test import TestCase
from django.urls import reverse
from .models import URL

class URLShortenerTests(TestCase):
    def test_create_url(self):
        """
        The test create new short URL and check if it exists
        """
        response = self.client.post(
            reverse('create_url'), 
            data={'url': 'https://example.com'}, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('short_url', data)
        self.assertTrue(URL.objects.filter(short_url=data['short_url'].split('/')[-1]).exists())

    def test_redirect_url(self):
        """
        The test create new object in the DB (known long and short URL),
        and check if the short URL redircet to the long one
        """
        URL.objects.create(long_url='https://example.com', short_url='test123')
        response = self.client.get(reverse('redirect_url', args=['test123']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://example.com')  # check the Location header

    def test_redirect_non_existing_url(self):
        response = self.client.get(reverse('redirect_url', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
