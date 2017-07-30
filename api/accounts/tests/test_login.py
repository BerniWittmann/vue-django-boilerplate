from django.test import TestCase
from api.accounts.models import MyUser
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
import json


class LoginTestCase(TestCase):
    def setUp(self):
        user = MyUser.objects.create(email='test@byom.de', first_name='Test', last_name='User')
        user.set_password('test123')
        user.is_verified = True
        user.save()

    def test_login_valid(self):
        client = APIClient()
        response = client.post(reverse('authemail-login'), {'email': 'test@byom.de', 'password': 'test123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIsNotNone(data['token'])

    def test_login_password_required(self):
        client = APIClient()
        response = client.post(reverse('authemail-login'), {'email': 'test@byom.de'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['password'], ['This field is required.'])

    def test_login_email_required(self):
        client = APIClient()
        response = client.post(reverse('authemail-login'), {'password': 'test123'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], ['This field is required.'])

    def test_login_email_invalid(self):
        client = APIClient()
        response = client.post(reverse('authemail-login'), {'email': 'not_an-E?mail', 'password': 'test123'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], ['Enter a valid email address.'])

    def test_login_invalid(self):
        client = APIClient()
        response = client.post(reverse('authemail-login'), {'email': 'test@byom.de', 'password': 'just_wrong'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Unable to login with provided credentials.')

    def test_login_unverified_user(self):
        user = MyUser.objects.first()
        user.is_verified = False
        user.save()

        client = APIClient()
        response = client.post(reverse('authemail-login'), {'email': 'test@byom.de', 'password': 'test123'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'User account not verified.')

    def test_login_inactive_user(self):
        user = MyUser.objects.first()
        user.is_active = False
        user.save()

        client = APIClient()
        response = client.post(reverse('authemail-login'), {'email': 'test@byom.de', 'password': 'test123'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn(data['detail'], ['User account not active.', 'Unable to login with provided credentials.'])
