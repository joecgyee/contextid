from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.serializers import UserRegistrationSerializer, UserLoginSerializer

class AccountTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@contextid.com',
            'password': 'securepassword123'
        }

    def test_assign_default_group_signal(self):
        """Test if users are automatically added to 'Users' group on creation."""
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.groups.filter(name='Users').exists())

    def test_user_registration_serializer(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')

    def test_user_login_serializer(self):
        User.objects.create_user(**self.user_data)
        login_data = {'username': 'testuser', 'password': 'securepassword123'}
        serializer = UserLoginSerializer(data=login_data)
        # Note: Depending on your implementation, this might require a request context
        self.assertTrue(serializer.is_valid())