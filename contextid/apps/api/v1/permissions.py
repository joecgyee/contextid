from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Only allow the owner of the object to edit/view it."""
    def has_object_permission(self, request, view, obj):
        # Handles User objects or objects with a .user attribute
        user_obj = getattr(obj, 'user', obj)
        return user_obj == request.user

class IsPublicOrOwnerOrAdmin(permissions.BasePermission):
    """
    - If public: Any authenticated user can GET.
    - If private: Only owner or admin can GET.
    - Updates/Delete: Only owner or admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.user == request.user or request.user.is_staff
        return obj.user == request.user or request.user.is_staff