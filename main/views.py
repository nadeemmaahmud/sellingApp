from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Unit, Service, Sell, PrivacyPolicy, TermsAndConditions, AboutUs
from .serializers import UnitSerializer, ServiceSerializer, SellSerializer, PrivacyPolicySerializer, TermsAndConditionsSerializer, AboutUsSerializer

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

class PrivacyPolicyView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            policy = PrivacyPolicy.objects.latest('effective_date')
            serializer = PrivacyPolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PrivacyPolicy.DoesNotExist:
            return Response({'message': 'No privacy policy found'}, status=status.HTTP_404_NOT_FOUND)

class TermsAndConditionsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            terms = TermsAndConditions.objects.latest('effective_date')
            serializer = TermsAndConditionsSerializer(terms)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TermsAndConditions.DoesNotExist:
            return Response({'message': 'No terms and conditions found'}, status=status.HTTP_404_NOT_FOUND)

class AboutUsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            about = AboutUs.objects.first()
            serializer = AboutUsSerializer(about)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AboutUs.DoesNotExist:
            return Response({'message': 'No about us information found'}, status=status.HTTP_404_NOT_FOUND)

class PrivacyPolicyManageView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        policies = PrivacyPolicy.objects.all().order_by('-effective_date')
        serializer = PrivacyPolicySerializer(policies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PrivacyPolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Privacy policy created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrivacyPolicyUpdateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        try:
            policy = PrivacyPolicy.objects.get(pk=pk)
            serializer = PrivacyPolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PrivacyPolicy.DoesNotExist:
            return Response({'error': 'Privacy policy not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            policy = PrivacyPolicy.objects.get(pk=pk)
            serializer = PrivacyPolicySerializer(policy, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Privacy policy updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PrivacyPolicy.DoesNotExist:
            return Response({'error': 'Privacy policy not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            policy = PrivacyPolicy.objects.get(pk=pk)
            serializer = PrivacyPolicySerializer(policy, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Privacy policy updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PrivacyPolicy.DoesNotExist:
            return Response({'error': 'Privacy policy not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            policy = PrivacyPolicy.objects.get(pk=pk)
            policy.delete()
            return Response({
                'message': 'Privacy policy deleted successfully'
            }, status=status.HTTP_200_OK)
        except PrivacyPolicy.DoesNotExist:
            return Response({'error': 'Privacy policy not found'}, status=status.HTTP_404_NOT_FOUND)

class TermsAndConditionsManageView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        terms = TermsAndConditions.objects.all().order_by('-effective_date')
        serializer = TermsAndConditionsSerializer(terms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TermsAndConditionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Terms and conditions created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TermsAndConditionsUpdateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        try:
            terms = TermsAndConditions.objects.get(pk=pk)
            serializer = TermsAndConditionsSerializer(terms)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TermsAndConditions.DoesNotExist:
            return Response({'error': 'Terms and conditions not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            terms = TermsAndConditions.objects.get(pk=pk)
            serializer = TermsAndConditionsSerializer(terms, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Terms and conditions updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TermsAndConditions.DoesNotExist:
            return Response({'error': 'Terms and conditions not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            terms = TermsAndConditions.objects.get(pk=pk)
            serializer = TermsAndConditionsSerializer(terms, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Terms and conditions updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TermsAndConditions.DoesNotExist:
            return Response({'error': 'Terms and conditions not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            terms = TermsAndConditions.objects.get(pk=pk)
            terms.delete()
            return Response({
                'message': 'Terms and conditions deleted successfully'
            }, status=status.HTTP_200_OK)
        except TermsAndConditions.DoesNotExist:
            return Response({'error': 'Terms and conditions not found'}, status=status.HTTP_404_NOT_FOUND)

class AboutUsManageView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        about = AboutUs.objects.all()
        serializer = AboutUsSerializer(about, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AboutUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'About us created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AboutUsUpdateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        try:
            about = AboutUs.objects.get(pk=pk)
            serializer = AboutUsSerializer(about)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AboutUs.DoesNotExist:
            return Response({'error': 'About us not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            about = AboutUs.objects.get(pk=pk)
            serializer = AboutUsSerializer(about, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'About us updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AboutUs.DoesNotExist:
            return Response({'error': 'About us not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            about = AboutUs.objects.get(pk=pk)
            serializer = AboutUsSerializer(about, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'About us updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AboutUs.DoesNotExist:
            return Response({'error': 'About us not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            about = AboutUs.objects.get(pk=pk)
            about.delete()
            return Response({
                'message': 'About us deleted successfully'
            }, status=status.HTTP_200_OK)
        except AboutUs.DoesNotExist:
            return Response({'error': 'About us not found'}, status=status.HTTP_404_NOT_FOUND)
