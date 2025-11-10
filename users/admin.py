from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Unit, Service, Sell, PrivacyPolicy, TermsAndConditions, AboutUs, EmailVerificationToken, PasswordResetOTP

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'phone', 'address', 'zip_code')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_verified', 'is_staff', 'is_active')}
        ),
    )
    
    readonly_fields = ['date_joined', 'last_login']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['vin', 'brand', 'model', 'year', 'user', 'status', 'created_at']
    list_filter = ['status', 'brand', 'year', 'created_at']
    search_fields = ['vin', 'brand', 'model', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['unit', 'appointment', 'status', 'cost', 'location', 'created_at']
    list_filter = ['status', 'past_history', 'appointment', 'created_at']
    search_fields = ['unit__vin', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-appointment']

@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ['unit', 'sale_price', 'sale_date', 'buyer_name', 'payment_method']
    list_filter = ['sale_date', 'payment_method']
    search_fields = ['unit__vin', 'buyer_name', 'buyer_email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-sale_date']

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'effective_date', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-effective_date']

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'effective_date', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-effective_date']

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_used', 'is_valid']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'otp_code']
    readonly_fields = ['otp_code', 'created_at', 'expires_at']
    ordering = ['-created_at']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_used', 'is_valid']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'otp_code']
    readonly_fields = ['otp_code', 'created_at', 'expires_at']
    ordering = ['-created_at']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'

admin.site.register(CustomUser, CustomUserAdmin)

