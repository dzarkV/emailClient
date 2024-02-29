from rest_framework.test import APITestCase
from rest_framework import status
from tests.factories.user_factory import UserFactory
from emailApp.serializers import UserSerializer

class TestCreateUser(APITestCase):
    """
    Class to test users' API creation endpoint
    """

    create_url = '/users/create'
    data = {
        "email": "test@mail.com",
        "password": "password",
        "name": "test"
    }

    def test_create_user_whole_data(self):
        """
        Test creating a user with complete data.

        Returns:
        - None
        """
        response = self.client.post(self.create_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

    def test_create_user_without_email(self):
        """
        Test creating a user without providing an email.

        Returns:
        - None
        """
        user = self.data.copy()
        user.pop('email')
        response = self.client.post(self.create_url, user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This field is required')

    def test_create_user_without_password(self):
        """
        Test creating a user without providing a password.

        Returns:
        - None
        """
        user = self.data.copy()
        user.pop('password')
        response = self.client.post(self.create_url, user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_existent_already(self):
        """
        Test creating a user with an email that already exists.

        Returns:
        - None
        """
        user = UserFactory().create_user()
        response = self.client.post(self.create_url, UserSerializer(user).data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Email already exists')
