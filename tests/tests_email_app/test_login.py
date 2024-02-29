from rest_framework.test import APITestCase
from tests.factories.user_factory import UserFactory
from emailApp.serializers import UserSerializer
from rest_framework import status
from django.test import tag

class TestLogin(APITestCase):
    """
    Class to test users' API login endpoint
    """

    login_url = '/users/login'

    @tag('login')
    def test_login(self):
        """
        Test logging in with valid credentials.

        Returns:
        - None
        """
        user = UserFactory().create_user()
        user.password = "password"
        response = self.client.post(self.login_url, UserSerializer(user).data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_empty(self):
        """
        Test logging in with empty data.

        Returns:
        - None
        """
        data = {}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_existent_email_wrong_password(self):
        """
        Test logging in with an existent email but wrong password.

        Returns:
        - None
        """
        user = UserFactory().create_user()
        user.password = 'wrong_password'
        user.email = 'email@vertech.com'
        response = self.client.post(self.login_url, UserSerializer(user).data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid email or password')