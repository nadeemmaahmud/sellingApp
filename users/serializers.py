from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Unit, Service, Sell, PrivacyPolicy, TermsAndConditions, AboutUs, EmailVerificationToken, PasswordResetOTP

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'phone', 'address', 'zip_code', 'date_of_birth']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
            zip_code=validated_data.get('zip_code'),
            date_of_birth=validated_data.get('date_of_birth'),
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_verified:
                raise serializers.ValidationError('Please verify your email address before logging in.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs

class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'date_of_birth', 
                  'phone', 'address', 'zip_code', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'email', 'is_active', 'is_staff', 'date_joined']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True, required=True, label="Confirm New Password", style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

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

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits.")
        return value

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
            if user.is_verified:
                raise serializers.ValidationError("This email is already verified.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

class VerifyResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password", style={'input_type': 'password'})

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs