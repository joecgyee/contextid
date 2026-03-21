from rest_framework import serializers
from .models import *

class PriorityRuleSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='get_name_display', read_only=True)
    class Meta:
        model = PriorityRule
        fields = ['id', 'name', 'display_name']

class ValueTypeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='get_name_display', read_only=True)
    class Meta:
        model = ValueType
        fields = ['id', 'name', 'display_name']

class ProfileAttributeSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField()
    # value_type = serializers.SlugRelatedField(
    #     slug_field='name', 
    #     queryset=ValueType.objects.all()
    # )

    class Meta:
        model = ProfileAttribute
        fields = [
            'key', 'value',
            # We keep these here so the Serializer still accepts them during POST/PUT
            'value_string', 'value_int', 'value_bool', 'value_date', 'value_url'
        ]
        extra_kwargs = {
            # Mark the specific value fields as write_only
            'value_string': {'write_only': True},
            'value_int': {'write_only': True},
            'value_bool': {'write_only': True},
            'value_date': {'write_only': True},
            'value_url': {'write_only': True},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Remove nulls (optional, but keeps things clean)
        return {k: v for k, v in rep.items() if v is not None}
    
class AttributeContextRuleSerializer(serializers.ModelSerializer):
    # We use these for "Details" view to show nested info
    priority_details = PriorityRuleSerializer(source='priority', read_only=True)
    
    class Meta:
        model = AttributeContextRule
        fields = ['id', 'attribute', 'context', 'priority', 'priority_details', 'is_active']