from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from emailApp.models.categories import Categories
from emailApp.models.message_from import MessageFrom
from emailApp.models.message_to import MessageTo
from emailApp.models.user import User
from emailApp.views.messages_filter import MessageViewFilter

class TestMessagesFilter(APITestCase):
    def setUp(self):
        self.user_from = User.objects.create(email='from@example.com', name='From User')
        self.user_to = User.objects.create(email='to@example.com', name='To User')
        self.category = Categories.objects.create(category_name='Test Category', color="#288384")
        self.message_from = MessageFrom.objects.create(
            subject='Test Subject',
            body='Test Body',
            isActive=True,
            from_user=self.user_from,
            category_id=self.category
        )
        self.message_to = MessageTo.objects.create(
            message_id=self.message_from,
            to_user=self.user_to
        )
        self.view = MessageViewFilter.as_view()

    def test_get_messages(self):
        request = APIRequestFactory().get('/messages/filterByCategory/', {'category_id': self.category.category_id, 'email': self.user_to.email})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_messages_no_params(self):
        request = APIRequestFactory().get('/messages/filterByCategory/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_messages_no_messages(self):
        request = APIRequestFactory().get('/messages/filterByCategory/', {'category_id': self.category.category_id, 'email': 'nonexistent@example.com'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_deactivate_message(self):
        request_data = {'message_id': self.message_from.id}
        request = APIRequestFactory().patch('/messages/filterByCategory/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_no_message_id(self):
        request = APIRequestFactory().patch('/messages/filterByCategory/', {}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    

