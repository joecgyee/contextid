from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.accounts.serializers import UserRegistrationSerializer, UserPublicSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    post=extend_schema(
        summary="Register a New User",
        description="Create a new user account."
    )
)
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Current User",
        description="Retrieve the logged-in user's profile."
    ),
    put=extend_schema(
        summary="Update Current User",
        description="Replace the logged-in user's profile with new data."
    ),
    patch=extend_schema(
        summary="Partially Update Current User",
        description="Update selected fields of the logged-in user's profile."
    )
)
class UserMeView(generics.RetrieveUpdateAPIView):
    """Handles GET and PUT for the logged-in user."""
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user