from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout #database
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseBadRequest
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



def intra_login_redirect(request):
    code = request.GET.get("code")
    if not code:
        print("Code is missing in the request")
        return redirect("https://localhost/")
    print("Received code:", code)
    try:
        user_data = exhange_code(code)
        if not user_data:
            raise ValueError("Failed to exchange code for user")
        print("Exchanged user:", user_data)
        intra_user = authenticate(request, user=user_data)
        if intra_user is None:
            print("Authentication failed")
        login(request, intra_user, backend='project.apps.intrauth.auth.IntraAuthenticationBackend')
        # print(f"User logged in successfully: {intra_user}")
        return redirect("https://localhost/mainpage")
    except Exception as e:
        print(f"Error during OAuth redirect: {e}")
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")

def exhange_code(code: str):
    token_url = "https://api.intra.42.fr/oauth/token"
    user_info_url = "https://api.intra.42.fr/v2/me"
    #token request data
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
    try:
        #request access token
        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()  #raise an exception for HTTP errors
        credentials = response.json()
        access_token = credentials['access_token']
        if not access_token:
            raise ValueError("Access token not found in response")
        #fetch user info
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(user_info_url, headers=headers)
        response.raise_for_status()
        user = response.json()
        print(f"Fetched user data: {user}")
        return user
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    # print (requests)
    # response = requests.post('https://api.intra.42.fr/oauth/token', data=data, headers=headers)
    # print("response will be")
    # print(response)
    # credentials = response.json()
    # access_token = credentials['access_token']
    # response = requests.get("https://api.intra.42.fr/v2/me", headers={
    #     'Authorization': 'Bearer %s' % access_token
    # })
    # print(response)
    # user = response.json()
    # print(user)
    # return user

