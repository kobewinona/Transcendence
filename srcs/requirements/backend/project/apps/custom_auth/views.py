# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .serializer import UserSerializer,  OTPRequestSerializer, OTPVerifySerializer
from django.contrib.auth import authenticate
import os
#otp verification
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import pyotp
import resend
import requests
from django.core.cache import cache
# from datetime import datetime, timedelta #


User = get_user_model()
###registration
class UserCreateView(APIView):
    authentication_classes = []  # disable authentication
    permission_classes = []  
    def get(self, request): # define endpoint function if i need info
        # return Response(UserSerializer(request.user).data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
###OTP creation    
    
resend = os.environ.get('RESEND') 

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # 5 minutes validity
    return totp.now()
def send_email(email, otp):
	url = 'https://api.resend.com/emails'
	headers = {
		'Authorization': f'Bearer {resend}',
		'Content-Type': 'application/json'
	}
	data = {
		"from": "onboarding <noreply@birgabon.me>",
		"to": [email],
		"subject": "Use it smartly",
		"html": f"<p>Dont loose it {otp}. We will never send it again</p>"
	}
	try:
		response = requests.post(url, headers=headers, json=data)
		if response.status_code == 200:
			print('Email sent successfully')
		else:
			print(f'Failed to send email: {response.status_code}')
			print(response.text)
	except Exception as e:
		print(f'Error sending email: {str(e)}')
        
class GetOTPView(APIView):

	def post(self, request):
     	# print('in api great')
		serializer = OTPRequestSerializer(data=request.data)
		if serializer.is_valid():
			username = serializer.validated_data['username']
			try:
				user = User.objects.get(username=username)
				otp = generate_otp()
				cache.set(f'otp_{username}', otp, timeout=300)  # save for 5 min in cashe
				print(f"Wow OTP is sent and is: {otp}")
				send_email(user.email, otp)
				return Response({'otp': otp}, status=status.HTTP_200_OK)
			except User.DoesNotExist:
				return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
	def post(self, request):
		serializer = OTPVerifySerializer(data=request.data)
		if serializer.is_valid():
			username = serializer.validated_data['username']
			received_otp = serializer.validated_data['otp']
			stored_otp = cache.get(f'otp_{username}')
			if stored_otp and received_otp == stored_otp:
				cache.delete(f'otp_{username}')
				return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
			return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint
    def get(self, request):
        return Response({'isAuthenticated': True})
    
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'logged out'})
        response.delete_cookie('refresh_token') #refresh token
        return response
    
    
    
    
    
    
    
    
    
    
    

# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(self, request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data) #for specific user

#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save() #update users info
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

