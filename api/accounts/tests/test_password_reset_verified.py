from django.test import TestCase
from api.accounts.models import MyUser
from django.contrib.auth import authenticate
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from authemail.models import PasswordResetCode
import json


class PasswordResetVerifiedTestCase(TestCase):
    code = None

    def setUp(self):
        user = MyUser.objects.create(email='test@byom.de', first_name='Test', last_name='User')
        user.set_password('test123')
        user.is_verified = True
        user.save()
        self.code = PasswordResetCode.objects.create_reset_code(user).code.decode('utf-8')

    def test_reset_password_verified_valid(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset-verified'),
                               {'code': self.code, 'password': 'new_password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['success'], 'Password reset.')
        user = authenticate(email='test@byom.de', password='new_password')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@byom.de')

    def test_reset_password_verified_code_required(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset-verified'),
                               {'password': 'new_password'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['code'], ['This field is required.'])

    def test_reset_password_verified_code_invalid(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset-verified'),
                               {'code': 'wrongcode', 'password': 'new_password'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Unable to verify user.')

    def test_reset_password_verified_password_required(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset-verified'),
                               {'code': self.code})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['password'], ['This field is required.'])

    def test_reset_password_verified_with_old_password(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset-verified'),
                               {'code': self.code, 'password': 'test123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['success'], 'Password reset.')

    def test_reset_password_verified_remove_code(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset-verified'),
                               {'code': self.code, 'password': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PasswordResetCode.objects.count(), 0)