from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer,ProfileSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = user.verification_token

            verification_link = request.build_absolute_uri(
                f"/accounts/verify/{token}/"
            )

            send_mail(
                subject="Verify your email",
                message=f"Click to verify your account: {verification_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "User created. Please verify your email."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VerifyEmailView(APIView):
    permission_classes = []

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            user.is_verified = True
            user.save()

            return Response(
                {"message": "Email verified successfully. You can now login."},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid or expired verification link"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)

        return Response(serializer.data,status=status.HTTP_200_OK)