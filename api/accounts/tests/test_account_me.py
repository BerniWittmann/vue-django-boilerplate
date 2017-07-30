from django.test import TestCase
from api.accounts.models import MyUser
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
import json
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AccountMeTestCase(TestCase):
    token = None

    def setUp(self):
        user = MyUser.objects.create(email='test@byom.de', first_name='Test', last_name='User')
        user.set_password('test123')
        user.is_verified = True
        user.save()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)

    def test_account_me_valid(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.get(reverse('authemail-me'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertFalse(data['is_staff'])

    def test_account_me_unauthorized(self):
        client = APIClient()
        response = client.get(reverse('authemail-me'))
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Authentication credentials were not provided.')

    def test_account_me_invalid_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT absolute_invalid_token')
        response = client.get(reverse('authemail-me'))
        self.assertEqual(response.status_code, 401)

    def test_account_me_staff(self):
        user = MyUser.objects.first()
        user.is_staff = True
        user.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.get(reverse('authemail-me'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertTrue(data['is_staff'])
