from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from emailApp.models.categories import Categories
from emailApp.models.message_from import MessageFrom
from emailApp.models.user import User
from emailApp.views.messages import MessageView

class TestMessageUpdateCategory(APITestCase):
    """
    Test cases for updating the category of a message through the API.
    """
    def setUp(self):
        """
        Set up test data and create an instance of the view.
        """
        self.user = User.objects.create(email='test@example.com')
        self.category = Categories.objects.create(category_name='Test Category', color="#288384")
        self.message = MessageFrom.objects.create(
            subject='Test Subject',
            body='Test Body',
            isActive=True,
            from_user=self.user,
            category_id=self.category
        )
        self.view = MessageView.as_view()

    def test_patch_message_category(self):
        """
        Test updating the category of a message.

        Returns:
        - None
        """
        new_category = Categories.objects.create(category_name='New Category', color="#123456")
        request_data = {'message_id': self.message.id, 'category_id': new_category.category_id}
        request = APIRequestFactory().patch('/message/updateCategory/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Message update successfully.')
        updated_message = MessageFrom.objects.get(id=self.message.id)
        self.assertEqual(updated_message.category_id, new_category)

    def test_patch_no_message_id(self):
        """
        Test updating the category without providing a message_id.

        Returns:
        - None
        """
        request_data = {'category_id': self.category.category_id}
        request = APIRequestFactory().patch('/message/updateCategory/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Both message_id and category_id are required for the patch operation.')

    def test_patch_no_category_id(self):
        """
        Test updating the category without providing a category_id.

        Returns:
        - None
        """
        request_data = {'message_id': self.message.id}
        request = APIRequestFactory().patch('/message/updateCategory/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Both message_id and category_id are required for the patch operation.')

    def test_patch_invalid_message_id(self):
        """
        Test updating the category with an invalid message_id.

        Returns:
        - None
        """
        invalid_message_id = self.message.id + 1000
        request_data = {'message_id': invalid_message_id, 'category_id': self.category.category_id}
        request = APIRequestFactory().patch('/message/updateCategory/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Message not found.')

    def test_patch_invalid_category_id(self):
        """
        Test updating the category with an invalid category_id.

        Returns:
        - None
        """
        invalid_category_id = self.category.category_id + 1000
        request_data = {'message_id': self.message.id, 'category_id': invalid_category_id}
        request = APIRequestFactory().patch('/message/updateCategory/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Category not found.')
