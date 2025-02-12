from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout #database
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import os

def home(request : HttpRequest) -> JsonResponse:
    return JsonResponse({"msg" : "success"})

@login_required(login_url="/oauth/login/") # change for login url


def get_authenticated_user(request : HttpRequest) : 
    return JsonResponse({"msg": "Authenticated"})

def intra_login(request : HttpRequest):
    client_id = os.getenv("CLIENT_ID")
    # redirect_uri = "https://localhost/game"
    redirect_uri = "http://localhost:8000/oauth/redirect"
    auth_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    print("Redirecting to:", auth_url)
    return redirect(auth_url)

def intra_login_redirect(request : HttpRequest):
    print("Im coming from redirect")
    if "code" not in request.GET:
        return redirect("https://localhost/")
    code = request.GET.get("code")
    print("Received code:", code)
    user = exhange_code(code)
    print("the request",request)
    intra_user = authenticate(request, user=user)
    intra_user = list(intra_user).pop()
    print("intra_user",intra_user)
    if intra_user is not None:
        login(request, intra_user)
        return redirect('https://localhost/')
    else:
        return Response({"error": "Authentication failed"}, status=400)
    # login(request, intra_user) #check session database
    # return redirect("/auth/user/")

def exhange_code(code: str):
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth/redirect/",
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    print (requests)
    response = requests.post('https://api.intra.42.fr/oauth/token', data=data, headers=headers)
    print("response will be")
    print(response)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://api.intra.42.fr/v2/me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    print(response)
    user = response.json()
    print(user)
    return user

