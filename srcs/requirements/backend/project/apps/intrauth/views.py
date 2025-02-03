from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import os

# Create your views here.

#put in an .env, maybe


def home(request : HttpRequest) -> JsonResponse:
    return JsonResponse({"msg" : "success"})

@login_required(login_url="/oauth/login/")

def get_authenticated_user(request : HttpRequest) :
    return JsonResponse({"msg": "Authenticated"})

def intra_login(request : HttpRequest):
    return redirect(os.getenv("AUTH_URL_INTRA"))

def intra_logout(request):
    logout(request)
    return redirect('https://localhost/')

@api_view(['GET'])
def intra_login_redirect(request : HttpRequest):
    if "code" not in request.GET:
        return redirect("https://localhost/")
    code = request.GET["code"]
    user = exchange_code(code)
    intra_user = authenticate(request, user=user)
    if intra_user is not None:
        login(request, intra_user)
        return redirect('https://localhost/')
    else:
        return Response({"error": "Authentication failed"}, status=400)

def exchange_code(code: str):
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post('https://api.intra.42.fr/oauth/token', data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://api.intra.42.fr/v2/me", headers={
        "Authorization": "Bearer " + access_token
    })
    user = response.json()
    return user

def is_logged_in(request):
    if request.user.is_authenticated:
        return JsonResponse({"is_logged_in": True})
    else:
        return JsonResponse({"is_logged_in": False})