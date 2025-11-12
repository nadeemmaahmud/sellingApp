from rest_framework import serializers
from .models import Unit, Service, Sell, PrivacyPolicy, TermsAndConditions, AboutUs

class UnitSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    services_count = serializers.IntegerField(source='services.count', read_only=True)
    
    class Meta:
        model = Unit
        fields = ['id', 'user', 'user_email', 'vin', 'brand', 'model', 'year', 'mileage', 
                  'date_of_purchase', 'location', 'status', 'additional_info', 'image', 
                  'services_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_vin(self, value):
        if len(value) != 17:
            raise serializers.ValidationError("VIN must be exactly 17 characters long.")
        if self.instance:
            if Unit.objects.filter(vin=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A unit with this VIN already exists.")
        else:
            if Unit.objects.filter(vin=value).exists():
                raise serializers.ValidationError("A unit with this VIN already exists.")
        return value.upper()

class ServiceSerializer(serializers.ModelSerializer):
    unit_info = serializers.CharField(source='unit.__str__', read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'unit', 'unit_info', 'description', 'location', 'appointment', 
                  'completion_date', 'cost', 'status', 'past_history', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('completion_date') and attrs.get('appointment'):
            if attrs['completion_date'] < attrs['appointment']:
                raise serializers.ValidationError("Completion date cannot be before appointment date.")
        return attrs

class SellSerializer(serializers.ModelSerializer):
    unit_info = serializers.CharField(source='unit.__str__', read_only=True)
    
    class Meta:
        model = Sell
        fields = ['id', 'unit', 'unit_info', 'sale_price', 'sale_date', 'buyer_name', 
                  'buyer_email', 'buyer_phone', 'payment_method', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_sale_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Sale price must be greater than zero.")
        return value

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