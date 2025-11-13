from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import PrivacyPolicy, TermsAndConditions, AboutUs
from .serializers import PrivacyPolicySerializer, TermsAndConditionsSerializer, AboutUsSerializer
from main.models import Service, Sell
from main.serializers import ServiceSerializer, SellSerializer
from users.serializers import CustomUserSerializer

CustomUser = get_user_model()

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

class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total_users = CustomUser.objects.count()
        
        services_today = Service.objects.filter(
            created_at__gte=today_start,
            created_at__lte=today_end
        ).count()

        sells_today = Sell.objects.filter(
            created_at__gte=today_start,
            created_at__lte=today_end
        ).count()
        
        recent_users = CustomUser.objects.all().order_by('-date_joined')[:limit]
        recent_users_serializer = CustomUserSerializer(recent_users, many=True)
        
        return Response({
            'total_users': total_users,
            'services_created_today': services_today,
            'sells_created_today': sells_today,
            'recent_users': recent_users_serializer.data,
            'date': timezone.now().date()
        }, status=status.HTTP_200_OK)

class AllUsersView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 10))
   
        users = CustomUser.objects.all().order_by('-date_joined')
 
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = CustomUserSerializer(paginated_users, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class UserSearchView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        search = request.query_params.get('q', '').strip()
        limit = int(request.query_params.get('limit', 10))
        
        if not search:
            return Response({
                'message': 'Please provide a search query using the "q" parameter',
                'results': []
            }, status=status.HTTP_200_OK)
      
        users = CustomUser.objects.filter(
            first_name__icontains=search
        ) | CustomUser.objects.filter(
            last_name__icontains=search
        ) | CustomUser.objects.filter(
            email__icontains=search
        ) | CustomUser.objects.filter(
            phone__icontains=search
        )
 
        users = users.order_by('-date_joined').distinct()[:limit]
        
        serializer = CustomUserSerializer(users, many=True)
        
        return Response({
            'count': users.count(),
            'search_query': search,
            'results': serializer.data
        }, status=status.HTTP_200_OK)

class AllServicesView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 10))

        services = Service.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_services = paginator.paginate_queryset(services, request)

        serializer = ServiceSerializer(paginated_services, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class AllSellsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 10))
        
        sells = Sell.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_sells = paginator.paginate_queryset(sells, request)

        serializer = SellSerializer(paginated_sells, many=True)
        
        return paginator.get_paginated_response(serializer.data)
