from django.test import TestCase
from django.db import IntegrityError
from .models import Context
from .serializers import ContextSerializer

class ContextTestCase(TestCase):
    def setUp(self):
        Context.objects.all().delete()
        Context.objects.create(name="Legal")
        Context.objects.create(name="Professional")
        Context.objects.create(name="Social")
        Context.objects.create(name="Cultural")
        Context.objects.create(name="Online")
    
    def test_contexts_created(self):
        # Check total count
        self.assertEqual(Context.objects.count(), 5)

        # Check that each expected context exists
        expected_names = ["Legal", "Professional", "Social", "Cultural", "Online"]
        actual_names = list(Context.objects.values_list("name", flat=True))
        for name in expected_names:
            self.assertIn(name, actual_names)

    def test_context_uniqueness(self):
        """Ensure that two contexts cannot have the same name."""
        # 'Legal' was already created in setUp
        with self.assertRaises(IntegrityError):
            Context.objects.create(name="Legal")

    from apps.contexts.serializers import ContextSerializer

    def test_context_serializer_output(self):
        """Verify that the serializer returns the correct fields."""
        context = Context.objects.get(name="Professional")
        serializer = ContextSerializer(context)
        
        expected_fields = {'id', 'name'} 
        self.assertTrue(expected_fields.issubset(set(serializer.data.keys())))
        self.assertEqual(serializer.data['name'], "Professional")
