from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Unit, Service, Sell, PrivacyPolicy, TermsAndConditions, AboutUs, EmailVerificationToken, PasswordResetOTP
from .serializers import (
    RegisterSerializer, LoginSerializer, CustomUserSerializer, 
    ChangePasswordSerializer,
    UnitSerializer, ServiceSerializer, SellSerializer,
    PrivacyPolicySerializer, TermsAndConditionsSerializer, AboutUsSerializer,
    EmailVerificationSerializer, ResendVerificationEmailSerializer,
    ForgotPasswordSerializer, VerifyResetOTPSerializer, ResetPasswordSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification_token = EmailVerificationToken.objects.create(user=user)
            email_subject = 'Verify Your Email - SellnService'
            email_message = f"""
                Hello {user.first_name},

                Thank you for registering with SellnService!

                Your email verification code is:

                {verification_token.otp_code}

                This code will expire in 15 minutes.

                If you didn't create an account, please ignore this email.

                Best regards,
                SellnService Team
            """
            
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@sellnservice.com',
                    [user.email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                print(f"Email sending failed: {e}")
                email_sent = False
            
            return Response({
                'message': 'User registered successfully. Please check your email for the verification code.',
                'user': CustomUserSerializer(user).data,
                'email_sent': email_sent,
                'otp_code': verification_token.otp_code if not email_sent else None
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': CustomUserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        return self.put(request)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                if user.is_verified:
                    return Response({
                        'message': 'Email is already verified. You can login now.'
                    }, status=status.HTTP_200_OK)
                
                verification_token = EmailVerificationToken.objects.filter(
                    user=user,
                    otp_code=otp_code,
                    is_used=False
                ).order_by('-created_at').first()
                
                if not verification_token:
                    return Response({
                        'error': 'Invalid verification code.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not verification_token.is_valid():
                    return Response({
                        'error': 'Verification code has expired. Please request a new one.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user.is_verified = True
                user.is_active = True
                user.save()
                
                verification_token.is_used = True
                verification_token.save()
                
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'message': 'Email verified successfully! You can now login.',
                    'user': CustomUserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
                
            except CustomUser.DoesNotExist:
                return Response({
                    'error': 'No user found with this email address.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            EmailVerificationToken.objects.filter(user=user, is_used=False).update(is_used=True)
            verification_token = EmailVerificationToken.objects.create(user=user)
            email_subject = 'Verify Your Email - SellnService'
            email_message = f"""
                Hello {user.first_name},

                You requested a new email verification code.

                Your verification code is:

                {verification_token.otp_code}

                This code will expire in 15 minutes.

                If you didn't request this, please ignore this email.

                Best regards,
                SellnService Team
            """
            
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@sellnservice.com',
                    [user.email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                print(f"Email sending failed: {e}")
                email_sent = False
            
            return Response({
                'message': 'Verification code sent successfully. Please check your email.',
                'email_sent': email_sent,
                'otp_code': verification_token.otp_code if not email_sent else None
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            PasswordResetOTP.objects.filter(user=user, is_used=False).update(is_used=True)
            reset_otp = PasswordResetOTP.objects.create(user=user)
            email_subject = 'Password Reset Request - SellnService'
            email_message = f"""
                Hello {user.first_name},

                You requested to reset your password.

                Your password reset code is:

                {reset_otp.otp_code}

                This code will expire in 15 minutes.

                If you didn't request this, please ignore this email and your password will remain unchanged.

                Best regards,
                SellnService Team
            """
            
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@sellnservice.com',
                    [user.email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                print(f"Email sending failed: {e}")
                email_sent = False
            
            return Response({
                'message': 'Password reset code sent to your email.',
                'email_sent': email_sent,
                'otp_code': reset_otp.otp_code if not email_sent else None
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyResetOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = VerifyResetOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            
            try:
                user = CustomUser.objects.get(email=email)
                reset_otp = PasswordResetOTP.objects.filter(
                    user=user,
                    otp_code=otp_code,
                    is_used=False
                ).order_by('-created_at').first()
                
                if not reset_otp:
                    return Response({
                        'error': 'Invalid reset code.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not reset_otp.is_valid():
                    return Response({
                        'error': 'Reset code has expired. Please request a new one.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    'message': 'OTP verified successfully. You can now reset your password.',
                    'email': email
                }, status=status.HTTP_200_OK)
                
            except CustomUser.DoesNotExist:
                return Response({
                    'error': 'No user found with this email address.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = CustomUser.objects.get(email=email)
                reset_otp = PasswordResetOTP.objects.filter(
                    user=user,
                    otp_code=otp_code,
                    is_used=False
                ).order_by('-created_at').first()
                
                if not reset_otp:
                    return Response({
                        'error': 'Invalid reset code.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not reset_otp.is_valid():
                    return Response({
                        'error': 'Reset code has expired. Please request a new one.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user.set_password(new_password)
                user.save()
                reset_otp.is_used = True
                reset_otp.save()
                
                return Response({
                    'message': 'Password reset successful! You can now login with your new password.'
                }, status=status.HTTP_200_OK)
                
            except CustomUser.DoesNotExist:
                return Response({
                    'error': 'No user found with this email address.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)