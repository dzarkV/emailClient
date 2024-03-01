from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.message_from import MessageFrom
from emailApp.models.message_to import MessageTo
from emailApp.models.categories import Categories

class TestGetAllMessages(APITestCase):
    """
    Test cases for retrieving all messages for a user through the API.
    """
    def setUp(self):
        """
        Set up test data and create an instance of APIClient.
        """
        self.user_from = User.objects.create(email='from@example.com', name='From User')
        self.user_to = User.objects.create(email='to@example.com', name='To User')
        self.client = APIClient()

    def test_get_messages(self):
        """
        Test retrieving messages for a valid user.

        Returns:
        - None
        """
        message_from = MessageFrom.objects.create(from_user=self.user_from, subject='Test Subject', body='Test Body', category_id=Categories.objects.get(category_id=0 ))
        message_to = MessageTo.objects.create(message_id=message_from, to_user=self.user_to)
        response = self.client.get('/messages/getAll', {'email': self.user_from.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message_id'], message_from.id)
        self.assertEqual(response.data[0]['from_user'], self.user_from.email)
        self.assertEqual(response.data[0]['to_user'], self.user_to.email)

    def test_get_messages_invalid_user(self):
        """
        Test retrieving messages for an invalid user.

        Returns:
        - None
        """
        response = self.client.get('/messages/getAll', {'mail': 'invalid@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_messages_multiple(self):
        """
        Test retrieving multiple messages for a user.

        Returns:
        - None
        """
        message_from1 = MessageFrom.objects.create(from_user=self.user_from, subject='Message 1', body='Body 1', category_id=Categories.objects.get(category_id=0))
        message_to1 = MessageTo.objects.create(message_id=message_from1, to_user=self.user_to)

        message_from2 = MessageFrom.objects.create(from_user=self.user_from, subject='Message 2', body='Body 2', category_id=Categories.objects.get(category_id=0))
        message_to2 = MessageTo.objects.create(message_id=message_from2, to_user=self.user_to)

        response = self.client.get('/messages/getAll', {'email': self.user_from.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


