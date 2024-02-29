from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from emailApp.models.user import User
from emailApp.models.categories import Categories
from emailApp.models.categories_users import CategoriesUser
from emailApp.views.categories import CategoryView

class TestCategory(APITestCase):
    """
    Test cases for the CategoryView API.
    """
    def setUp(self):
        """
        Set up test data and create an instance of CategoryView.
        """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='test@example.com')
        self.category_data = {'category_name': 'Test Category', 'color': '#827833', 'email': 'test@example.com'}
        self.category_view = CategoryView.as_view()

    def test_get_categories(self):
        """
        Test retrieving categories for a valid user.

        Returns:
        - None
        """
        Categories.objects.create(category_name='Category1')
        Categories.objects.create(category_name='Category2')
        CategoriesUser.objects.create(email=self.user, category_id=Categories.objects.first())

        request = self.factory.get('/category/getAll/', {'email': 'test@example.com'})
        response = self.category_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_categories_invalid_email(self):
        """
        Test retrieving categories with an invalid user email.

        Returns:
        - None
        """
        request = self.factory.get('/category/getAll/', {'email': 'invalid@example.com'})
        response = self.category_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_category(self):
        """
        Test creating a new category.

        Returns:
        - None
        """
        request = self.factory.post('/category/create/', self.category_data)
        response = self.category_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_data(self):
        """
        Test creating a new category with invalid data.

        Returns:
        - None
        """
        invalid_data = {'invalid_field': 'Invalid Data'}
        request = self.factory.post('/category/create/', invalid_data)
        response = self.category_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
