from django.urls import path
from .views import UnitListCreateView, UnitDetailView, ServiceListCreateView, ServiceDetailView, SellListCreateView, SellDetailView, PrivacyPolicyView, TermsAndConditionsView, AboutUsView

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
]