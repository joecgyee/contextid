from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.profiles.models import IdentityProfile
from apps.profiles.serializers import IdentityProfileSerializer
from ..permissions import *
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(
        summary="List Profiles",
        description="Retrieve all public profiles (plus your own if authenticated)."
    ),
    retrieve=extend_schema(
        summary="Retrieve a Profile",
        description="Retrieve a single profile by ID."
    ),
    create=extend_schema(
        summary="Create a Profile",
        description="Create a new profile."
    ),
    update=extend_schema(
        summary="Update a Profile",
        description="Replace an existing profile with new data."
    ),
    partial_update=extend_schema(
        summary="Partially Update a Profile",
        description="Update selected fields of an existing profile."
    ),
    destroy=extend_schema(
        summary="Delete a Profile",
        description="Permanently remove a profile."
    ),
    me=extend_schema(
        summary="Manage My Profiles",
        description=(
            "GET /api/v1/profiles/me/ → List all my profiles (public or private).\n"
            "POST /api/v1/profiles/me/ → Create a profile for myself."
        )
    )
)
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = IdentityProfileSerializer
    permission_classes = [IsPublicOrOwnerOrAdmin]

    def get_queryset(self):
        """
        Global visibility logic:
        1. Staff/Admins see everything.
        2. Authenticated users see public profiles OR their own private profiles.
        3. Unauthenticated users see only public profiles.
        """
        user = self.request.user
        queryset = IdentityProfile.objects.select_related('context').prefetch_related('attributes')

        if user.is_staff:
            return queryset

        if user.is_authenticated:
            # Show if (public) OR (belongs to me)
            return queryset.filter(Q(is_public=True) | Q(user=user))
        
        # Public only for guests
        return queryset.filter(is_public=True)

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated, IsOwner])
    def me(self, request):

        if request.method == 'GET':
            # This calls the filtered get_queryset() above, then narrows it further to 'me'
            profiles = self.get_queryset().filter(user=request.user)
            
            context_name = request.query_params.get('context')
            if context_name:
                profiles = profiles.filter(context__name__iexact=context_name)
                
            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)