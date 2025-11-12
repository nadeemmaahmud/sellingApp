from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

CustomUser = get_user_model()

class Unit(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('in_service', 'In Service'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='units')
    vin = models.CharField(max_length=17, unique=True, help_text='Vehicle Identification Number (17 characters)')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    mileage = models.IntegerField(null=True, blank=True, help_text='Current mileage')
    date_of_purchase = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    additional_info = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='unit_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['-created_at']

    def clean(self):
        if self.vin and len(self.vin) != 17:
            raise ValidationError({'vin': 'VIN must be exactly 17 characters long.'})

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} - {self.vin}"

class Service(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='services')
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    appointment = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    past_history = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-appointment']

    def __str__(self):
        return f"Service for {self.unit.vin} on {self.appointment}"

class Sell(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='sales')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(default=timezone.now)
    buyer_name = models.CharField(max_length=100, null=True, blank=True)
    buyer_email = models.EmailField(null=True, blank=True)
    buyer_phone = models.CharField(max_length=15, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale of {self.unit.vin} on {self.sale_date}"

class PrivacyPolicy(models.Model):
    content = models.TextField()
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'
        ordering = ['-effective_date']

    def __str__(self):
        return f"Privacy Policy - {self.effective_date}"

class TermsAndConditions(models.Model):
    content = models.TextField()
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Terms and Conditions'
        verbose_name_plural = 'Terms and Conditions'
        ordering = ['-effective_date']

    def __str__(self):
        return f"Terms and Conditions - {self.effective_date}"

class AboutUs(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return "About Us"
