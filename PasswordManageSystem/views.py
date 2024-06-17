from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import get_user_model
from MyApplication.tools import *
from MyApplication.exception import *
from .models import *
# Create your views here.


def index(request, context=None):
    if context is None:
        context = {}
    success = request.session.get('success', -1)
    error = request.session.get('error', -1)
    if success == 1:
        context['success'] = True
        info = request.session.get('info')
        context['info'] = info
        del request.session['success']
    elif success == 0:
        context['success'] = False
        if error != -1:
            print_line('error:' + str(error))
            context['error'] = error
            del request.session['error']

    username = request.session.get('username', False)
    if username:
        # print("Username is" + username)
        context['usernameflag'] = True
        context['username'] = username
    else:
        context['usernameflag'] = False
        return render(request, "login.html")
    system_user_name = username
    system_user = get_user_model()
    user = system_user.objects.get(username=system_user_name)
    pwdinfo = user.password_info.all().order_by('-id')

    # 分页
    p = Paginator(pwdinfo, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "pm/index.html", context)


def test1(request):
    system_user_name = 'gaopeng'
    system_user = get_user_model()
    user = system_user.objects.get(username=system_user_name)

    # for i in range(0, 40):
    #     uname = "guge112"+str(i)
    #     p1 = PasswordInfo(name=uname, username='alice', password='123')
    #     p1.owner = user
    #     p1.save()
    print_line("success")
    return index(request)


def test2(request):

    return index(request)


def add_record(request):
    if request.method == "POST":
        p_name = request.POST.get('appname')
        p_username = request.POST.get('username')
        p_password = request.POST.get('password')
        p_phone_number = request.POST.get('phone_number')
        p_email = request.POST.get('email')
        p_website = request.POST.get('website')
        p_notes = request.POST.get('notes')
        print(p_name, p_username, p_password, p_phone_number, p_email, p_website, p_notes, sep='|')
        try:
            if p_name == '':
                raise CustomError("应用名称不能为空")
            if p_username == '':
                raise CustomError("用户名不能为空")
            if p_password == '':
                raise CustomError("密码不能为空")
            system_user_name = request.session.get('username')
            print_line("system_user_name")
            print(system_user_name)
            system_user = get_user_model()
            user = system_user.objects.get(username=system_user_name)

            pwd_info = PasswordInfo(name=p_name,
                                    username=p_username,
                                    password=p_password,
                                    phone_number=p_phone_number,
                                    email=p_email,
                                    website=p_website,
                                    notes=p_notes)
            pwd_info.owner = user
            pwd_info.save()
            request.session['info'] = "添加记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    # return index(request)
    return redirect("/PasswordManage/index/")


def delete_record(request, pid):
    try:
        pwd_info = PasswordInfo.objects.get(pk=pid)

        pwd_info.delete()
        # 处理结果，如果需要的话
        request.session['info'] = "记录【" + str(pid) + "】删除成功"
        request.session['success'] = 1
    except Exception as e:
        # 捕获其他类型的异常
        request.session['error'] = str(e)
        request.session['success'] = 0
    return redirect("/PasswordManage/index/")


def edit_record(request, pid):
    if request.method == "POST":
        p_name = request.POST.get('appname')
        p_username = request.POST.get('username')
        p_password = request.POST.get('password')
        p_phone_number = request.POST.get('phone_number')
        p_email = request.POST.get('email')
        p_website = request.POST.get('website')
        p_notes = request.POST.get('notes')
        try:
            if p_name == '':
                raise CustomError("应用名称不能为空")
            if p_username == '':
                raise CustomError("用户名不能为空")
            if p_password == '':
                raise CustomError("密码不能为空")
            pwd_info = PasswordInfo.objects.get(pk=pid)
            pwd_info.name = p_name
            pwd_info.username = p_username
            pwd_info.password = p_password
            pwd_info.phone_number = p_phone_number
            pwd_info.email = p_email
            pwd_info.website = p_website
            pwd_info.notes = p_notes
            pwd_info.save()
            request.session['info'] = "修改记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    return redirect("/PasswordManage/index/")


def search(request, context=None):
    if context is None:
        context = {}
    success = request.session.get('success', -1)
    error = request.session.get('error', -1)
    if success == 1:
        context['success'] = True
        info = request.session.get('info')
        context['info'] = info
        del request.session['success']
    elif success == 0:
        context['success'] = False
        if error != -1:
            print_line('error:' + str(error))
            context['error'] = error
            del request.session['error']

    username = request.session.get('username', False)
    if username:
        context['usernameflag'] = True
        context['username'] = username
    else:
        context['usernameflag'] = False
        return render(request, "login.html")
    system_user_name = username
    system_user = get_user_model()
    user = system_user.objects.get(username=system_user_name)
    pwdinfo = user.password_info.all().order_by('-id')
    if request.method == "POST":
        search_content = request.POST.get('searchname')
        pwdinfo = pwdinfo.filter(name__icontains=search_content).order_by('-id')

    # 分页
    p = Paginator(pwdinfo, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "pm/index.html", context)
