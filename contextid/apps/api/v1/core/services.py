from apps.profiles.models import IdentityProfile

def resolve_identity(target_username, context_name, requester):
    """
    Business logic to find a profile and check privacy.
    """
    profile = IdentityProfile.objects.filter(
        user__username=target_username,
        context__name__iexact=context_name
    ).first()

    if not profile:
        return None, "Profile not found for this context."

    # Check Privacy
    if not profile.is_public and profile.user != requester and not requester.is_staff:
        return None, "Access Denied: This profile is private."

    return profile, None