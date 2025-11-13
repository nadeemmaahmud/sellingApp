from django.db import models
from django.utils import timezone

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
