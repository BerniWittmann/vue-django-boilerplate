from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class HomeTestCase(TestCase):
    def test_page_is_served(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html>', status_code=200)
        self.assertContains(response, '<head>', status_code=200)
        self.assertContains(response, '<body>', status_code=200)
        self.assertContains(response, '</html>', status_code=200)
        self.assertContains(response, '</head>', status_code=200)
        self.assertContains(response, '</body>', status_code=200)

    def test_page_is_served_sub_url(self):
        client = Client()
        response = client.get(reverse('home') + 'sub_page/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html>', status_code=200)
        self.assertContains(response, '<head>', status_code=200)
        self.assertContains(response, '<body>', status_code=200)
        self.assertContains(response, '</html>', status_code=200)
        self.assertContains(response, '</head>', status_code=200)
