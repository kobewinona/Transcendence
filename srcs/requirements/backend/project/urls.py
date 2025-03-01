from django.http import HttpResponse
from django.contrib import admin
from django.urls import path


def home(request):
    return HttpResponse("Hello, Django is running!")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
]
