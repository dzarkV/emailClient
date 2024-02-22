from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.message_from import MessageFrom
from emailApp.models.message_to import MessageTo

class Test_get_messages(APITestCase):
    def setUp(self):
        self.user_from = User.objects.create(email='from@example.com', name='From User')
        self.user_to = User.objects.create(email='to@example.com', name='To User')
        self.client = APIClient()

    def test_get_messages(self):
        message_from = MessageFrom.objects.create(from_user=self.user_from, subject='Test Subject', body='Test Body', category_id=1)
        message_to = MessageTo.objects.create(message_id=message_from, to_user=self.user_to)
        response = self.client.get('/messages/getAll', {'mail': self.user_from.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['message_id'], message_from.id)
        self.assertEqual(response.data[0]['from_user'], self.user_from.email)
        self.assertEqual(response.data[0]['to_user'], self.user_to.email)

    def test_get_messages_invalid_user(self):
        response = self.client.get('/messages/getAll', {'mail': 'invalid@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      

