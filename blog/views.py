from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import blog.models as m

# Create your views here.

def login(request):
    if request.method =="GET":
        return render(request,"login.html")
    elif request.method =="POST":
        user = request.POST["user"]
        password = request.POST["password"]
        user = authenticate(username=user, password=password)
        if user is not None:
            auth_login(request, user)
        return HttpResponseRedirect('/home/')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/home/')

def homePage(request):
    posts = m.Post.objects.all()
    if request.method =="GET":
        #if request.user
        return render(request,"home.html")

def post(request):
    if request.method =="POST":
        user = request.user
        content = request.POST["content"]
        p = m.Post()
        p.author = user
        p.content = content
        p.visiability = m.Post.VISIABILITY
        return HttpResponseRedirect('/home/')