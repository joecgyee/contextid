from django.test import TestCase
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from apps.contexts.models import Context
from apps.profiles.models import IdentityProfile

class ProfileCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass')
        self.context = Context.objects.create(name='TEST')
        self.profile_data = {
            'user': self.user,
            'context': self.context,
            'display_name': 'Testing',
            'is_public': True
        }

    def tearDown(self):
        User.objects.all().delete()
        Context.objects.all().delete()

    def test_profile_creation(self):
        profile = IdentityProfile.objects.create(**self.profile_data)
        self.assertEqual(profile.display_name, 'Testing')
        self.assertTrue(profile.is_public)

    def test_profile_update(self):
        profile = IdentityProfile.objects.create(**self.profile_data)
        profile.display_name = 'Updated Name'
        profile.save()
        self.assertEqual(IdentityProfile.objects.get(id=profile.id).display_name, 'Updated Name')

    def test_unique_user_context_constraint(self):
        """Verify that a user cannot create a second profile for the same context."""
        # Create the first profile
        IdentityProfile.objects.create(user=self.user, context=self.context, display_name="First")
        
        # Attempt to create the second profile for the same user/context
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityProfile.objects.create(user=self.user, context=self.context, display_name="Second") 

    def test_profile_behavior_on_user_delete(self):
        """Test if profiles are correctly handled (Cascaded) when a user is deleted."""
        profile = IdentityProfile.objects.create(**self.profile_data)
        profile.save()
        user_id = self.user.id
        self.user.delete()

        # Check if the profile was also deleted (assuming on_delete=models.CASCADE)
        profile_exists = IdentityProfile.objects.filter(user_id=user_id).exists()
        self.assertFalse(profile_exists, "Profile should be deleted when the user is deleted.")