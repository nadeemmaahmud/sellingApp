from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Unit, Service, Sell
from admin.models import PrivacyPolicy, TermsAndConditions, AboutUs
from .serializers import UnitSerializer, ServiceSerializer, SellSerializer
from admin.serializers import PrivacyPolicySerializer, TermsAndConditionsSerializer, AboutUsSerializer

class UnitListCreateView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Unit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Unit.objects.filter(user=self.request.user)

class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        unit_id = self.request.query_params.get('unit_id')
        queryset = Service.objects.filter(unit__user=self.request.user)
        if unit_id:
            queryset = queryset.filter(unit_id=unit_id)
        return queryset

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Service.objects.filter(unit__user=self.request.user)

class SellListCreateView(generics.ListCreateAPIView):
    serializer_class = SellSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Sell.objects.filter(unit__user=self.request.user)
    
    def perform_create(self, serializer):
        sell = serializer.save()
        sell.unit.status = 'sold'
        sell.unit.save()

class SellDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Sell.objects.filter(unit__user=self.request.user)
