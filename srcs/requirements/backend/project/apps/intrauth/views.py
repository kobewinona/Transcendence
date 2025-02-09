from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import os

def home(request : HttpRequest) -> JsonResponse:
    return JsonResponse({"msg" : "success"})

@login_required(login_url="/oauth/login/")
# for future when will add field for the baseuser(only via email now           )
def get_authenticated_user(request : HttpRequest) : 
    return JsonResponse({"msg": "Authenticated"})

def intra_login(request : HttpRequest):
    return redirect(os.getenv("AUTH_URL_INTRA"))

def intra_logout(request):
    logout(request)
    return redirect('https://localhost/')
# 
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
    
    
    
    # def oauth_42(req):
    # if req.user.is_authenticated:
    #     return JsonResponse({'message': 'User is already authenticated'})
    # # try:
    # client_id = os.environ["CLIENT_ID"]
    # client_secret = os.environ["CLIENT_SECRET"]
    # redirect_uri = "https://localhost:8443/oauth_42"
    # code = req.GET.get("code")
    # state = req.GET.get("state")
    # csrf_token = get_token(req)
    # oauth = OAuth2Session(
    #     client_id,
    #     redirect_uri=redirect_uri
    # )
    # if not code:
    #     req.session['_next'] = req.GET.get("next", "/home")
    #     authorization_url, state = oauth.authorization_url(
    #         'https://api.intra.42.fr/oauth/authorize',
    #         kwargs = {
    #             'csrfToken': csrf_token
    #         }
    #     )
    #     return redirect(authorization_url)
    #     # return JsonResponse({'redirect_uri': authorization_url})
    # elif state:
    #     token = oauth.fetch_token(
    #         'https://api.intra.42.fr/oauth/token',
    #         client_secret=client_secret,
    #         code=code,
    #         kwargs = {
    #             'csrfToken': csrf_token
    #         }
    #     )
    #     user_data = oauth.get('https://api.intra.42.fr/v2/me').json()
    #     if User.objects.filter(email=user_data.get('email')).exists():
    #         return oauth_login(req, user_data)
    #     else:
    #         return oauth_register(req, oauth, user_data)
    # # except Exception as error:
    # #     return redirect("/")
    #     # return JsonResponse({'message': type(error).__name__})
    # return redirect("/")
    # return JsonResponse({'message': 'Oauth fatal error'})