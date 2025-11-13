from django.urls import path
from .views import (
    PrivacyPolicyView, 
    TermsAndConditionsView, 
    AboutUsView,
    DashboardStatsView,
    AllUsersView,
    UserSearchView,
    AllServicesView,
    AllSellsView
)

urlpatterns = [
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('users/', AllUsersView.as_view(), name='all-users'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('services/', AllServicesView.as_view(), name='all-services'),
    path('sells/', AllSellsView.as_view(), name='all-sells'),
]
