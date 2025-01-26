# # from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# # from .serializer import UserSerializer

# #create endpounts 

# @api_view(['GET']) #define request
# def get_users(request): # define endpoint function if i need info
#     # return Response(UserSerializer(request.user).data)
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

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


# def index(request)
#     return JsonResponse({"message": "Welcome to Custom Auth!"})



# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
# import json

# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import authenticate, login, logout
# from .serializer import CreateUserForm


# @ensure_csrf_cookie
# @require_http_methods(['GET'])
# def set_csrf_token(request):
#     """
#     We set the CSRF cookie on the frontend.
#     """
#     return JsonResponse({'message': 'CSRF cookie set'})


# @require_http_methods(['POST'])
# def login_view(request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         email = data['email']
#         password = data['password']
#     except json.JSONDecodeError:
#         return JsonResponse(
#             {'success': False, 'message': 'Invalid JSON'}, status=400
#         )

#     user = authenticate(request, username=email, password=password)

#     if user:
#         login(request, user)
#         return JsonResponse({'success': True})
#     return JsonResponse(
#         {'success': False, 'message': 'Invalid credentials'}, status=401
#     )


# def logout_view(request):
#     logout(request)
#     return JsonResponse({'message': 'Logged out'})


# @require_http_methods(['GET'])
# def user(request):
#     if request.user.is_authenticated:
#         return JsonResponse(
#             {'username': request.user.username, 'email': request.user.email}
#         )
#     return JsonResponse(
#         {'message': 'Not logged in'}, status=401
#     )


# @require_http_methods(['POST'])
# def register(request):
#     data = json.loads(request.body.decode('utf-8'))
#     form = CreateUserForm(data)
#     if form.is_valid():
#         form.save()
#         return JsonResponse({'success': 'User registered successfully'}, status=201)
#     else:
#         errors = form.errors.as_json()
#         return JsonResponse({'error': errors}, status=400)



# from django.http import HttpRequest, HttpResponse, JsonResponse
# from django.shortcuts import redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# import requests
# import os

# # Create your views here.

# #put in an .env, maybe


# def home(request : HttpRequest) -> JsonResponse:
#     return JsonResponse({"msg" : "success"})

# @login_required(login_url="/oauth/login/")

# def get_authenticated_user(request : HttpRequest) :
#     return JsonResponse({"msg": "Authenticated"})

# def intra_login(request : HttpRequest):
#     return redirect(os.getenv("AUTH_URL_INTRA"))

# def intra_logout(request):
#     logout(request)
#     return redirect('https://localhost:443/')

# @api_view(['GET'])
# def intra_login_redirect(request : HttpRequest):
#     if "code" not in request.GET:
#         return redirect("https://localhost:443/")
#     code = request.GET["code"]
#     user = exchange_code(code)
#     intra_user = authenticate(request, user=user)
#     if intra_user is not None:
#         login(request, intra_user)
#         return redirect('https://localhost:443/')#8081
#     else:
#         return Response({"error": "Authentication failed"}, status=400)

# def exchange_code(code: str):
#     data = {
#         "client_id": os.getenv("CLIENT_ID"),
#         "client_secret": os.getenv("CLIENT_SECRET"),
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": os.getenv("REDIRECT_URI"),
#         "scope": "identify"
#     }
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     response = requests.post('https://api.intra.42.fr/oauth/token', data=data, headers=headers)
#     credentials = response.json()
#     access_token = credentials['access_token']
#     response = requests.get("https://api.intra.42.fr/v2/me", headers={
#         "Authorization": "Bearer " + access_token
#     })
#     user = response.json()
#     return user

# def is_logged_in(request):
#     if request.user.is_authenticated:
#         return JsonResponse({"is_logged_in": True})
#     else:
#         return JsonResponse({"is_logged_in": False})