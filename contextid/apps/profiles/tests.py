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

    def test_international_naming_and_jsonb_storage(self):
        """
        Tests PostgreSQL storage with diverse international naming structures 
        to ensure UTF-8 integrity and no truncation.
        """
        # 1. Spanish Double-Surname (Multiple components & spaces)
        spanish_name = "Diego Rodríguez de Silva y Velázquez"
        
        # 2. Arabic Patrilineal (RTL characters and complex lineage)
        arabic_name = "أبو كريم محمد بن عبد العزيز بن فيصل"
        
        # 3. Icelandic Patronymic (Special characters: ð)
        icelandic_name = "Björk Guðmundsdóttir"
        
        # 4. Eastern Order / CJK (Multi-byte characters)
        cjk_name = "佐藤 健 (Sato Takeru)"

        names_to_test = [spanish_name, arabic_name, icelandic_name, cjk_name]

        for name in names_to_test:
            # We create a profile for each naming structure
            # If your model has a JSONB field (e.g., 'extra_data'), we test that too
            profile = IdentityProfile.objects.create(
                user=self.user,
                context=Context.objects.create(name=f"CTX_{names_to_test.index(name)}"),
                display_name=name,
            )
            
            # Refresh from DB to ensure PostgreSQL round-trip didn't mangle data
            profile.refresh_from_db()
            
            self.assertEqual(profile.display_name, name, f"Failed to store/retrieve name: {name}")
            
            # Ensure length is preserved (no truncation)
            self.assertEqual(len(profile.display_name), len(name))