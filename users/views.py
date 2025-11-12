from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, EmailVerificationToken, PasswordResetOTP
from .serializers import (
    RegisterSerializer, LoginSerializer, CustomUserSerializer, 
    ChangePasswordSerializer, EmailVerificationSerializer, ResendVerificationEmailSerializer,
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
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                EmailVerificationToken.objects.filter(user=user).delete()
                user.delete()
                return Response({
                    'error': 'Failed to send verification email. Please try again later.',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'message': 'User registered successfully. Please check your email for the verification code.',
                'user': CustomUserSerializer(user).data
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
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({
                    'error': 'Failed to send verification email. Please try again later.',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'message': 'Verification code sent successfully. Please check your email.'
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
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({
                    'error': 'Failed to send password reset email. Please try again later.',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'message': 'Password reset code sent to your email.'
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