from rest_framework.test import APITestCase
from rest_framework import status
from tests.factories.user_factory import UserFactory

class TestGetUsers(APITestCase):
    """
    Class to test users' API get all users endpoint
    """

    get_users_url = '/users/'

    def test_get_users(self):
        """
        Test retrieving all users.

        Returns:
        - None
        """
        UserFactory().create_user()
        response = self.client.get(self.get_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_by_email(self):
        """
        Test retrieving a user by email.

        Returns:
        - None
        """
        user = UserFactory().create_user()
        response = self.client.get(self.get_users_url + f'?email={user.email}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)

    def test_get_user_by_not_found_email(self):
        """
        Test retrieving a user with a non-existent email.

        Returns:
        - None
        """
        response = self.client.get(self.get_users_url + f'?email=something@mail.com')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Email user not found')