from django.test import TestCase
from api.accounts.models import MyUser
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.core import mail
import json
from authemail.models import SignupCode


class SignupTestCase(TestCase):
    def test_signup_valid(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de', 'password': 'test123', 'first_name': 'Test',
                                'last_name': 'User'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')

    def test_signup_email_required(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'password': 'test123', 'first_name': 'Test',
                                'last_name': 'User'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], ['This field is required.'])

    def test_signup_password_required(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de', 'first_name': 'Test',
                                'last_name': 'User'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['password'], ['This field is required.'])

    def test_signup_first_name_optional(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de',
                                'last_name': 'User', 'password': 'test123'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')
        self.assertEqual(data['first_name'], '')
        self.assertEqual(data['last_name'], 'User')

    def test_signup_last_name_optional(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de',
                                'first_name': 'Test', 'password': 'test123'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], '')

    def test_signup_only_email_and_password(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de', 'password': 'test123'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')
        self.assertEqual(data['first_name'], '')
        self.assertEqual(data['last_name'], '')

    def test_signup_code_created(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de', 'password': 'test123', 'first_name': 'Test',
                                'last_name': 'User'})
        self.assertEqual(response.status_code, 201)
        user_id = MyUser.objects.first().id
        signup_code = SignupCode.objects.filter(user=user_id)
        self.assertEqual(len(signup_code), 1)
        self.assertIsNotNone(signup_code.first().code)

    def test_signup_email_sent(self):
        client = APIClient()
        response = client.post(reverse('authemail-signup'),
                               {'email': 'test@byom.de', 'password': 'test123', 'first_name': 'Test',
                                'last_name': 'User'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Verify your email address')
