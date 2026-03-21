from django.contrib import admin
from .models import *
from apps.attributes.models import ProfileAttribute

class ProfileAttributeInline(admin.TabularInline):
    """
    Allows you to add/edit attributes (like 'Nickname') 
    directly inside the Identity Profile screen.
    """
    model = ProfileAttribute
    extra = 0
    fields = ('key', 'value_type', 'get_effective_value')
    readonly_fields = ('get_effective_value', 'created_at',)
    show_change_link = True  # Adds a link to the full Attribute edit page
    
    def get_effective_value(self, obj):
        """Displays the non-null value from the correct column."""
        if obj.value_int is not None:
            return obj.value_int
        if obj.value_bool is not None:
            return obj.value_bool
        if obj.value_date is not None:
            return obj.value_date
        if hasattr(obj, 'value_url') and obj.value_url is not None:
            return obj.value_url
        return obj.value_string or "-"
    get_effective_value.short_description = 'Value'


@admin.register(IdentityProfile)
class IdentityProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'context', 'display_name', 'is_public', 'created_at')
    list_filter = ('context', 'is_public', 'created_at')
    search_fields = ('user__username', 'user__email', 'display_name')
    readonly_fields = ('created_at', 'updated_at')
    
    # This connects the inline we defined above
    inlines = [ProfileAttributeInline]
    
    fieldsets = (
        ('Identity Info', {
            'fields': ('user', 'context', 'display_name', 'profile_pic', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )