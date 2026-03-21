from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.profiles.models import IdentityProfile
from apps.contexts.models import Context

class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.username = "api_user"
        self.password = "SecurePass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # Adjust this URL name based on your actual accounts urls.py
        self.login_url = "/api/v1/login/" 

    def test_full_jwt_auth_cycle(self):
        """Test obtaining a token and using it to access a protected endpoint."""
        # Obtain Token
        login_response = self.client.post(self.login_url, {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data['access']

        # Use Token in Header for a protected request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        protected_url = "/api/v1/accounts/me/" 
        response = self.client.get(protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class APITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='password123')
        self.admin = User.objects.create_superuser(username='admin', password='password123')
        self.public_user = User.objects.create_user(username='stranger', password='password123')
        
        self.test_context, _ = Context.objects.get_or_create(name='TEST')        
        self.legal_context, _ = Context.objects.get_or_create(name='LEGAL')

        self.private_profile = IdentityProfile.objects.create(
            user=self.owner, 
            context=self.test_context, 
            display_name="Private Profile", 
            is_public=False
        )
        self.legal_profile = IdentityProfile.objects.create(
            user=self.owner, 
            context=self.legal_context, 
            display_name="Legal Information", 
            is_public=True
        )

        self.url = f'/api/v1/identity/?user={self.owner.username}&context={self.test_context.name}'

    # Permissions Tests
    def test_private_profile_access_denied_for_public(self):
        """Strangers should not be able to resolve a private profile."""
        self.client.force_authenticate(user=self.public_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_private_profile_access_allowed_for_admin(self):
        """Admins should bypass privacy for resolution."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Context-Resolution Accuracy Tests
    def test_accurate_context_profile_retrieval(self):
        """
        Verify that resolution only returns data for the requested context.
        Information from other contexts (like LEGAL) must not leak.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url) # Querying 'TEST' context
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the display_name belongs to 'TEST', not 'LEGAL'
        self.assertEqual(response.data['display_name'], "Private Profile")
        self.assertNotEqual(response.data['display_name'], "Legal Information")
