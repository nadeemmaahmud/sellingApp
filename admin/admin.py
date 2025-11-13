from django.contrib import admin
from .models import PrivacyPolicy, TermsAndConditions, AboutUs


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'effective_date', 'created_at', 'updated_at']
    list_filter = ['effective_date', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-effective_date']
    
    fieldsets = (
        ('Content', {
            'fields': ('content',)
        }),
        ('Dates', {
            'fields': ('effective_date', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'effective_date', 'created_at', 'updated_at']
    list_filter = ['effective_date', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-effective_date']
    
    fieldsets = (
        ('Content', {
            'fields': ('content',)
        }),
        ('Dates', {
            'fields': ('effective_date', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    class Meta:
        verbose_name = 'Terms and Conditions'
        verbose_name_plural = 'Terms and Conditions'


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('content',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'
