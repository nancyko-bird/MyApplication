from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .tools import *
from .exception import *


# Create your views here.


def index(request, context=None):
    if context is None:
        context = {}
    username = request.session.get('username', False)
    if username:
        context['usernameflag'] = True
        context['username'] = username
    else:
        context['usernameflag'] = False
        return render(request, "login.html")
    return render(request, "index.html", context)


def login(request, context=None):
    if context is None:
        return render(request, 'login.html')
    if 'username' in request.session:
        # 从会话中删除'username'
        del request.session['username']
    return render(request, 'login.html', context)


def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            if username == '' or password == '':
                raise CustomError("请输入用户名与密码！！！")
            user = authenticate(username=username, password=password)
            if user is not None:
                # 用户名和密码正确
                request.session['username'] = str(user)
                return redirect('/index')
            else:
                context['error'] = '用户名或密码错误'
                return render(request, "login.html", context)
                # 用户名或密码错误
        except Exception as e:
            context['error'] = str(e)
    return render(request, 'login.html', context)


def register(request, context=None):
    if context is None:
        return render(request, 'register.html')
    return render(request, 'register.html', context)


def user_register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        try:
            if username == '' or password == '':
                raise CustomError("请输入用户名与密码！！！")
            if password != confirm_password:
                raise CustomError("两次密码不一致！！！")
            user = User.objects.get(username=username)
            if user is not None:
                # context['register_success'] = '0'
                context['register_error'] = '注册失败'
                context['register_info'] = '用户名已存在，是否前往登录？'
                return render(request, "register.html", context)

        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)
            user.save()
            context['register_success'] = '注册成功'
            context['register_info'] = '注册成功，是否前往登录？'
            return render(request, "register.html", context)
        except Exception as e:
            context['error'] = str(e)
    return render(request, 'register.html', context)


def delsession():
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()
