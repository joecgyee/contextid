from django.contrib import admin
from .models import *

@admin.register(PriorityRule)
class PriorityRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(ValueType)
class ValueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    ordering = ('id',)
    
class AttributeContextRuleInline(admin.TabularInline):
    """
    Allows editing rules (e.g., 'Hide this in Social context')
    directly inside the Attribute screen.
    """
    model = AttributeContextRule
    extra = 1
    autocomplete_fields = ['context', 'priority']

@admin.register(ProfileAttribute)
class ProfileAttributeAdmin(admin.ModelAdmin):
    # Custom method to show the actual value across different columns
    list_display = ('id', 'get_profile_owner', 'get_context', 'key', 'value_type', 'get_effective_value')
    list_filter = ('value_type', 'profile__context')
    search_fields = ('key', 'profile__user__username', 'profile__display_name')
    
    inlines = [AttributeContextRuleInline]

    def get_profile_owner(self, obj):
        return obj.profile.user.username
    get_profile_owner.short_description = 'User'

    def get_context(self, obj):
        return obj.profile.context.name
    get_context.short_description = 'Context'

    def get_effective_value(self, obj):
        """Displays the non-null value from the correct column."""
        if obj.value_int is not None: return obj.value_int
        if obj.value_bool is not None: return obj.value_bool
        if obj.value_date is not None: return obj.value_date
        if obj.value_url is not None: return obj.value_url
        return obj.value_string or "-"
    get_effective_value.short_description = 'Value'

@admin.register(AttributeContextRule)
class AttributeContextRuleAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'context', 'priority', 'is_active')
    list_filter = ('context', 'priority', 'is_active')
    search_fields = ('attribute__key', 'attribute__profile__user__username')