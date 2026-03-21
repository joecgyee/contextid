from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.contexts.models import Context
from apps.contexts.serializers import ContextSerializer

from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(
        summary="(Public) List Contexts",
        description="Retrieve all available contexts."
    ),
    retrieve=extend_schema(
        summary="(Public) Retrieve a Context",
        description="Retrieve a specific context by ID."
    ),
    create=extend_schema(
        summary="(Admin-only) Create a Context",
        description="Create a new context."
    ),
    update=extend_schema(
        summary="(Admin-only) Update a Context",
        description="Replace an existing context."
    ),
    partial_update=extend_schema(
        summary="(Admin-only) Partially Update a Context",
        description="Update selected fields of a context."
    ),
    destroy=extend_schema(
        summary="(Admin-only) Delete a Context",
        description="Permanently remove a context."
    )
)
class ContextViewSet(viewsets.ModelViewSet):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer

    def get_permissions(self):
        """
        Logic:
        - list & retrieve: AllowAny (Everyone can see)
        - create, update, partial_update, destroy: IsAdminUser (Only Admins)
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]