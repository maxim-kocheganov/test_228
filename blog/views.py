from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def login(request):
    if request.method =="GET":
        return render(request,"login.html")
    elif request.method =="POST":
        user = request.POST["user"]
        password = request.POST["password"]
        user = authenticate(username=user, password=password)
        pass