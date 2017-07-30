from django.test import TestCase
from api.accounts.models import MyUser
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.core import mail
from authemail.models import PasswordResetCode
import json


class PasswordResetTestCase(TestCase):
    def setUp(self):
        user = MyUser.objects.create(email='test@byom.de', first_name='Test', last_name='User')
        user.set_password('test123')
        user.is_verified = True
        user.save()

    def test_reset_password_valid(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset'),
                               {'email': 'test@byom.de'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['email'], 'test@byom.de')

    def test_reset_password_unkown_email(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset'),
                               {'email': 'some_strange@email.com'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Password reset not allowed.')

    def test_reset_password_unverified(self):
        user = MyUser.objects.first()
        user.is_verified = False
        user.save()

        client = APIClient()
        response = client.post(reverse('authemail-password-reset'),
                               {'email': 'test@byom.de'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Password reset not allowed.')

    def test_reset_password_code(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset'),
                               {'email': 'test@byom.de'})
        self.assertEqual(response.status_code, 201)
        reset_code = PasswordResetCode.objects.first()
        self.assertIsNotNone(reset_code)

    def test_reset_password_email_sent(self):
        client = APIClient()
        response = client.post(reverse('authemail-password-reset'),
                               {'email': 'test@byom.de'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset Your Password')
