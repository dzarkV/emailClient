from rest_framework.test import APITestCase
from tests.factories.user_factory import UserFactory
from emailApp.serializers import UserSerializer
from rest_framework import status

class TestLogin(APITestCase):
    """
    Class to test users' API login endpoint
    """

    login_url = '/users/login'

    def test_login(self):
        user = UserFactory().create_user()
        response = self.client.post(self.login_url, UserSerializer(user).data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_empty(self):
        data = {}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_existent_email_wrong_password(self):
        user = UserFactory().create_user()
        user.password = 'wrong_password'
        response = self.client.post(self.login_url, UserSerializer(user).data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid email or password')