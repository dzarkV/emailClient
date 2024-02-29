from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.message_from import MessageFrom
from emailApp.models.message_to import MessageTo
from unittest.mock import patch

class Test_create_message(APITestCase):
    """
    Test cases for creating messages through the API.
    """
    def setUp(self):
        """
        Set up test data and create an instance of APIClient.
        """
        self.user_from = User.objects.create(email='from@example.com', name='From User')
        self.user_to = User.objects.create(email='to@example.com', name='To User')
        self.client = APIClient()

    def test_create_message(self):
        """
        Test creating a message with valid data.

        Returns:
        - None
        """
        data = {
            'subject': 'Test Subject',
            'body': 'Test Body',
            'from_user': self.user_from.email,
            'to_user': self.user_to.email
        }
        response = self.client.post('/messages/create', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MessageFrom.objects.filter(subject='Test Subject').exists())
        self.assertTrue(MessageTo.objects.filter(to_user=self.user_to).exists())
      
    def test_create_message_invalid_users(self):
        """
        Test creating a message with invalid user emails.

        Returns:
        - None
        """
        data = {
            'subject': 'Test Subject',
            'body': 'Test Body',
            'from_user': 'invalid_from@example.com',
            'to_user': 'invalid_to@example.com'
        }
        response = self.client.post('/messages/create', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_create_message_exception_handling(self):
        """
        Test exception handling during message creation.

        Returns:
        - None
        """
        with patch('emailApp.serializers.message_from_serializer.MessageFromSerializer.save') as mock_save:
            mock_save.side_effect = Exception("Simulated error")
            data = {
                'subject': 'Test Subject',
                'body': 'Test Body',
                'from_user': self.user_from.email,
                'to_user': self.user_to.email
            }
            response = self.client.post('/messages/create', data)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Simulated error", str(response.data))
        self.assertFalse(MessageFrom.objects.filter(subject='Test Subject').exists())
        self.assertFalse(MessageTo.objects.filter(to_user=self.user_to).exists())