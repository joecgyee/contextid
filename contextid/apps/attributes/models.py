from django.db import models
from apps.profiles.models import IdentityProfile
from apps.contexts.models import Context


class PriorityRule(models.Model):
    class Choices(models.TextChoices):
        DEFAULT = 'DEFAULT', 'Default'
        OVERRIDE = 'OVERRIDE', 'Override'
        FALLBACK = 'FALLBACK', 'Fallback'
        # overrides = PriorityRule.objects.filter(name=PriorityRule.Choices.OVERRIDE)
    
    name = models.CharField(
        max_length=30, 
        unique=True, 
        choices=Choices.choices, 
        default=Choices.DEFAULT
    )

    def __str__(self):
        return self.get_name_display()

class ValueType(models.Model):
    class Types(models.TextChoices):
        STRING = 'STRING', 'String'
        DATE = 'DATE', 'Date'
        INT = 'INT', 'Integer'
        URL = 'URL', 'URL'
        BOOLEAN = 'BOOLEAN', 'Boolean'

    name = models.CharField(
        max_length=30, 
        unique=True, 
        choices=Types.choices, 
        default=Types.STRING
    )

    def __str__(self):
        return self.get_name_display()
    
class ProfileAttribute(models.Model):
    """
    Attributes like gender, DOB, nickname, etc.
    """
    profile = models.ForeignKey(
        IdentityProfile,
        on_delete=models.CASCADE,
        related_name="attributes"
    )

    key = models.CharField(max_length=100)
    value_type = models.ForeignKey(
        ValueType,
        on_delete=models.PROTECT
    )

    value_string = models.CharField(max_length=500, blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
    value_url = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "key")

    def __str__(self):
        return f"{self.key} ({self.profile})"
    
    @property
    def value(self):
        """Returns the actual value based on value_type."""
        if self.value_int is not None: return self.value_int
        if self.value_bool is not None: return self.value_bool
        if self.value_date is not None: return self.value_date
        if self.value_url is not None: return self.value_url
        return self.value_string


class AttributeContextRule(models.Model):
    """
    Defines how an attribute behaves in a given context.
    """
    attribute = models.ForeignKey(
        ProfileAttribute,
        on_delete=models.CASCADE,
        related_name="context_rules"
    )
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE
    )
    priority = models.ForeignKey(
        PriorityRule,
        on_delete=models.PROTECT
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("attribute", "context")

    def __str__(self):
        return f"{self.attribute.key} → {self.context} ({self.priority})"

