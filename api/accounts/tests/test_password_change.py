from django.test import TestCase
from api.accounts.models import MyUser
from django.contrib.auth import authenticate
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
import json
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class PasswordChangeTestCase(TestCase):
    token = None

    def setUp(self):
        user = MyUser.objects.create(email='test@byom.de', first_name='Test', last_name='User')
        user.set_password('test123')
        user.is_verified = True
        user.save()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)

    def test_change_password_valid(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post(reverse('authemail-password-change'),
                               {'password': 'new_password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['success'], 'Password changed.')
        user = authenticate(email='test@byom.de', password='new_password')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@byom.de')

    def test_change_password_required(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post(reverse('authemail-password-change'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['password'], ['This field is required.'])

    def test_change_password_with_old_password(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post(reverse('authemail-password-change'),
                               {'password': 'test123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['success'], 'Password changed.')
        user = authenticate(email='test@byom.de', password='test123')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@byom.de')

    def test_change_password_unauthorized(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-change'),
                               {'password': 'new_password'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Authentication credentials were not provided.')

    def test_change_password_token_invalid(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT notavalidtoken')
        response = client.post(reverse('authemail-password-change'),
                               {'password': 'new_password'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Error decoding signature.')
