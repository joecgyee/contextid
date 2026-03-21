from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from apps.contexts.models import Context
from apps.profiles.models import IdentityProfile
from .models import ProfileAttribute, ValueType
from .serializers import ProfileAttributeSerializer

class AttributeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.context = Context.objects.create(name="TEST")
        self.profile = IdentityProfile.objects.create(user=self.user, context=self.context)
        self.type_string, _ = ValueType.objects.get_or_create(name="STRING")
        self.type_int, _ = ValueType.objects.get_or_create(name="INT")

    def test_cascade_delete_profile(self):
        """Test that deleting a profile also removes its attributes."""
        ProfileAttribute.objects.create(
            profile=self.profile, 
            key="Bio", 
            value_type=self.type_string, 
            value_string="Hello world"
        )
        
        self.assertEqual(ProfileAttribute.objects.count(), 1)
        
        # Delete the profile
        self.profile.delete()
        
        # Attribute should be gone
        self.assertEqual(ProfileAttribute.objects.count(), 0)

    def test_duplicate_attribute_key_per_profile(self):
        """Test that a profile cannot have two attributes with the same key name."""
        ProfileAttribute.objects.create(
            profile=self.profile, 
            key="Gender", 
            value_type=self.type_string, 
            value_string="Non-binary"
        )
        
        # Attempting to create another "Gender" key for the SAME profile should fail
        with self.assertRaises(IntegrityError):
            ProfileAttribute.objects.create(
                profile=self.profile, 
                key="Gender", 
                value_type=self.type_string, 
                value_string="Something else"
            )
    
    def test_serializer_output_is_clean(self):
        """
        Verify that the serializer hides internal value_type/value_int fields 
        and only outputs 'key' and 'value'.
        """
        attribute = ProfileAttribute.objects.create(
            profile=self.profile,
            key="Age",
            value_type=self.type_int,
            value_int=25
        )
        
        serializer = ProfileAttributeSerializer(attribute)
        data = serializer.data

        # Check that the core fields exist
        self.assertEqual(data['key'], "Age")
        self.assertEqual(data['value'], 25)

        # Ensure internal database fields are NOT in the output (Write-Only)
        hidden_fields = ['value_type', 'value_string', 'value_bool', 'value_date', 'value_url']
        for field in hidden_fields:
            self.assertNotIn(field, data, f"Internal field '{field}' should be hidden in API output.")

    def test_serializer_removes_nulls(self):
        """Verify that the to_representation logic strips null values from the response."""
        attribute = ProfileAttribute.objects.create(
            profile=self.profile,
            key="Website",
            value_type=self.type_string,
            value_string="https://contextid.com"
        )
        
        serializer = ProfileAttributeSerializer(attribute)
        # If value_int is None, it should not appear in the keys at all
        self.assertNotIn('value_int', serializer.data)