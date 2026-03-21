from django.db import transaction
from rest_framework import serializers
from .models import IdentityProfile
from apps.contexts.models import Context
from apps.attributes.models import ProfileAttribute
from apps.attributes.serializers import ProfileAttributeSerializer

class IdentityProfileSerializer(serializers.ModelSerializer):
    # Rename 'id' to 'profile_id'
    profile_id = serializers.ReadOnlyField(source='id')
    
    # Show the username instead of the user ID
    user = serializers.ReadOnlyField(source='user.username')
    
    # SlugRelatedField allows us to use 'name' (e.g., "LEGAL") 
    # for both GET and POST/PUT operations.
    context = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Context.objects.all()
    )
    
    attributes = ProfileAttributeSerializer(many=True, required=False)

    profile_pic_url = serializers.SerializerMethodField()

    class Meta:
        model = IdentityProfile
        fields = [
            'profile_id', 'user', 'context', 'display_name', 
            'attributes', 'profile_pic_url', 'is_public', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_profile_pic_url(self, obj):
        return obj.get_profile_pic_url

    def create(self, validated_data):
        # Extract the attributes data from the validated payload
        attributes_data = validated_data.pop('attributes', [])
        
        # Use a transaction to ensure data integrity
        with transaction.atomic():
            # Create the main profile
            profile = IdentityProfile.objects.create(**validated_data)
            
            # Create each attribute linked to this new profile
            for attr_data in attributes_data:
                ProfileAttribute.objects.create(profile=profile, **attr_data)
        
        return profile

    def validate(self, data):
        """
        Validation still works perfectly because SlugRelatedField 
        resolves the name string back into a Context object automatically.
        """
        user = self.context['request'].user
        context = data.get('context')
        
        exists = IdentityProfile.objects.filter(user=user, context=context)
        if self.instance:
            exists = exists.exclude(pk=self.instance.pk)
            
        if exists.exists():
            # context is now the object, so context.name works
            raise serializers.ValidationError(
                f"You already have a profile for the {context.name} context."
            )
        return data