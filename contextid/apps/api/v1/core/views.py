from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .services import resolve_identity
from apps.profiles.serializers import IdentityProfileSerializer

class IdentityResolutionView(APIView):
    @extend_schema(
        summary="[CORE] Resolve Context-Aware Identity",
        description="Retrieve a specific identity profile based on the target user and the interaction context.",
        parameters=[
            OpenApiParameter(
                name='user', 
                description='The username of the person whose identity you are requesting.', 
                required=True, 
                type=OpenApiTypes.STR, 
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='context', 
                description='e.g., LEGAL, PROFESSIONAL', 
                required=False, 
                type=OpenApiTypes.STR, 
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='X-Identity-Context', 
                description='The context name provided via Header (alternative to query param).', 
                required=False, 
                type=OpenApiTypes.STR, 
                location=OpenApiParameter.HEADER
            ),
        ],
        responses={200: IdentityProfileSerializer}
    )

    def get(self, request):
        target_user = request.query_params.get('user')
        # Check header first, then query param for context
        context_name = request.headers.get('X-Identity-Context') or request.query_params.get('context')

        if not target_user or not context_name:
            return Response({"error": "Missing user or context"}, status=400)

        profile, error = resolve_identity(target_user, context_name, request.user)
        
        if error:
            return Response({"detail": error}, status=403 if "Denied" in error else 404)

        serializer = IdentityProfileSerializer(profile)
        return Response(serializer.data)