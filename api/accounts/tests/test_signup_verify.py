from django.test import TestCase
from api.accounts.models import MyUser
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
import json
from authemail.models import SignupCode


class SignupVerifyTestCase(TestCase):
    user_id = None
    signup_code = None

    def setUp(self):
        user = MyUser.objects.create(email='test@byom.de', first_name='Test', last_name='User')
        user.set_password('test123')
        user.save()
        self.user_id = user.id
        self.signup_code = SignupCode.objects.create_signup_code(user=user, ipaddr='127.0.0.1').code.decode('utf-8')

    def test_signup_code_verify_valid(self):
        client = APIClient()
        response = client.get(reverse('authemail-signup-verify'),
                               {'code': self.signup_code})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['success'], 'User verified.')

    def test_signup_code_verify_empty(self):
        client = APIClient()
        response = client.get(reverse('authemail-signup-verify'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Unable to verify user.')

    def test_signup_code_verify_invalid(self):
        client = APIClient()
        response = client.get(reverse('authemail-signup-verify'),
                               {'code': 'totallywrong'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['detail'], 'Unable to verify user.')

    def test_signup_code_verify_remove_code(self):
        client = APIClient()
        response = client.get(reverse('authemail-signup-verify'),
                               {'code': self.signup_code})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SignupCode.objects.count(), 0)