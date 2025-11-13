from rest_framework import serializers
from .models import PrivacyPolicy, TermsAndConditions, AboutUs

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['id', 'content', 'effective_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ['id', 'content', 'effective_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']