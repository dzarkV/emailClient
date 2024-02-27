from emailApp.models import User


class UserFactory:
    """
    Factory to create (inside database testing) user objects before needed test
    """

    def build_user_JSON(self):
        return {
            "email": "test@mail.com",
            "password": "password",
            "name": "test"
        }
    
    def create_user(self) -> User:
        user = self.build_user_JSON()
        return User.objects.create_user(**user)
