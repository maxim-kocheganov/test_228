from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import blog.models as m
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
import re
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
        else:
            return render(request,"error.html",{'error' : "log"})
        return HttpResponseRedirect('/home/')

def register(request):
    if request.method =="GET":
        return render(request,"register.html")
    elif request.method =="POST":     
        User = get_user_model()
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            validate_email(email)
            alreadyExist = User.objects.filter(email = email).count()
        except:
            return 
        if alreadyExist == 0 and re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            user = User.objects.create_user(email=email,
                                 password=password)
            user.role = User.REGISTRED
            user.save()
        else:
            return render(request,"error.html",{'error' : "reg"})
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
        if request.user.is_anonymous:
            posts = posts.filter(visiability = m.Post.ALL)
        elif request.user.role == User.REGISTRED or request.user.is_staff == True\
            or request.user.role == User.AUTOR:
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
        post = m.Post.objects.filter(id = id)[0]
        if post.visiability == m.Post.ALL:
            pass
        else:
            if request.user.is_anonymous:
                raise Http404
            elif request.user.role == User.REGISTRED or request.user.is_staff == True\
                or request.user.role == User.AUTOR:
                pass
            else:
                raise Http404
        p = {'title':post.title,
            'author':post.author,
            'content':post.content,
            'edit':'/edit/' + str(post.id),
            'delete': '/delete/' + str(post.id)}
        return render(request,"show.html",p)

def edit(request, id):
    if request.method == "GET":    
        user = request.user
        User = get_user_model()
        post = m.Post.objects.filter(id = id)[0]
        if (request.user.is_anonymous == False and user.role == User.AUTOR and post.author == user)\
            or (user.is_staff == True):
            if (post.visiability == 'ALL'):
                for_all = "on"
            else:
                for_all = "off"            
            p = {'title':post.title,\
                 'content':post.content,\
                 'for_all':for_all}
            return render(request,"edit.html",p)     
        else:
            raise Http404()   
    if request.method =="POST":
        user = request.user
        User = get_user_model()
        p = m.Post.objects.filter(author = user).filter(id = id)[0]
        if ( request.user.is_anonymous == False and\
            user.role == User.AUTOR and  p.author == user)\
            or user.is_staff == True:
            content = request.POST["content"]            
            title = request.POST.get("title", "")
            p.content = content
            p.title = title
            for_all = request.POST.get("for_all", "off")
            if for_all == 'on':
                p.visiability = m.Post.REG
            elif for_all == 'off':
                p.visiability = m.Post.ALL
            p.save()
        else:
            raise Http404
        return HttpResponseRedirect('/home/')

def post(request):
    if request.method == "GET":        
        return render(request,"post.html")        
    if request.method =="POST":
        user = request.user
        User = get_user_model()
        if user.is_anonymous == False and (user.role == User.AUTOR or user.is_staff == True):
            content = request.POST["content"]
            title = request.POST.get("title", "")
            p = m.Post()
            p.author = user
            p.content = content
            p.title = title
            for_all = request.POST.get("for_all", "off")
            if for_all == 'on':
                p.visiability = m.Post.ALL
            elif for_all == 'off':
                p.visiability = m.Post.REG
            p.save()
        else:
            raise Http404(request)
        return HttpResponseRedirect('/home/')

def delete(request,id):
    if request.method == "GET":    
        user = request.user
        User = get_user_model()
        post = m.Post.objects.filter(id = id)[0]
        if (request.user.is_anonymous == False and user.role == User.AUTOR and post.author == user)\
            or user.is_staff == True:           
            p = {'id':id}
            return render(request,"delete.html",p)     
        else:
            raise Http404()   
    if request.method =="POST":
        user = request.user
        User = get_user_model()
        p = m.Post.objects.filter(author = user).filter(id = id)[0]
        if ( request.user.is_anonymous == False and\
            user.role == User.AUTOR and  p.author == user)\
            or user.is_staff == True:
            p.delete()
        else:
            raise Http404
        return HttpResponseRedirect('/home/')