from django.urls import path
from .views import (
    UnitListCreateView, UnitDetailView, 
    ServiceListCreateView, ServiceDetailView, 
    SellListCreateView, SellDetailView, 
    PrivacyPolicyView, TermsAndConditionsView, AboutUsView,
    PrivacyPolicyManageView, PrivacyPolicyUpdateView,
    TermsAndConditionsManageView, TermsAndConditionsUpdateView,
    AboutUsManageView, AboutUsUpdateView
)

urlpatterns = [
    path('units/', UnitListCreateView.as_view(), name='unit-list-create'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('sales/', SellListCreateView.as_view(), name='sell-list-create'),
    path('sales/<int:pk>/', SellDetailView.as_view(), name='sell-detail'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('admin/privacy-policy/', PrivacyPolicyManageView.as_view(), name='admin-privacy-policy'),
    path('admin/privacy-policy/<int:pk>/', PrivacyPolicyUpdateView.as_view(), name='admin-privacy-policy-detail'),
    path('admin/terms-and-conditions/', TermsAndConditionsManageView.as_view(), name='admin-terms-conditions'),
    path('admin/terms-and-conditions/<int:pk>/', TermsAndConditionsUpdateView.as_view(), name='admin-terms-conditions-detail'),
    path('admin/about-us/', AboutUsManageView.as_view(), name='admin-about-us'),
    path('admin/about-us/<int:pk>/', AboutUsUpdateView.as_view(), name='admin-about-us-detail'),
]