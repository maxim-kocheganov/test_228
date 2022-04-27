from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import blog.models as m
from django.contrib.auth import get_user_model

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
    User = get_user_model()
    if request.method =="GET":
        if request.user.role == User.REGISTRED or request.user.is_staff == True:
            posts = posts.all()
        else:
            posts = posts.filter(visiability = m.Post.ALL)
        displayPosts = []
        for post in posts:
            p = {'title':post.title,
                 'author':post.author,
                 'content':post.content,
                 'view': '/show/' + str(post.id),
                 'edit': '/edit/' + str(post.id),
                 'delete': '/delete/' + str(post.id)
                 }
            displayPosts.append(p)   
        return render(request,"home.html",{"displayPosts":displayPosts})

def show(request,id):
    User = get_user_model()
    if request.method =="GET":
        if request.user.role == User.REGISTRED or request.user.is_staff == True:
            post = m.Post.objects.filter(id = id)[0]
        else:
            return Http404()
        p = {'title':post.title,
            'author':post.author,
            'content':post.content,
            'edit':'/edit/' + str(post.id),
            'delete': '/delete/' + str(post.id)}
        return render(request,"show.html",p)

def edit(request, id):
    pass

def post(request):
    if request.method == "GET":        
        return render(request,"post.html")        
    if request.method =="POST":
        user = request.user
        User = get_user_model()
        if user.role == User.AUTOR or user.is_staff == True:
            content = request.POST["content"]
            p = m.Post()
            p.author = user
            p.content = content
            if request.POST["for_all"] == 'on':
                p.visiability = m.Post.REG
            elif request.POST["for_all"] == 'off':
                p.visiability = m.Post.ALL
            p.save()
        return HttpResponseRedirect('/home/')