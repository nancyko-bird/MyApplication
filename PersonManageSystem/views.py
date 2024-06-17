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
    person_info = user.owner.all().order_by('-id')

    # 分页
    p = Paginator(person_info, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "person/index.html", context)


def test1(request):
    system_user_name = 'gaopeng'
    system_user = get_user_model()
    user = system_user.objects.get(username=system_user_name)

    for i in range(0, 40):
        uname = "ALice"+str(i)
        u_pid = "ALice"+str(i)
        u_birth = "1996"+str(i)
        u_birth_address = "jinan"+str(i)
        u_age = "1"+str(i)
        u_gender = '2'+str(i)
        u_address = "qingdao"+str(i)
        u_phone = "178365214"+str(i)
        u_identity = '司机'+str(i)
        u_relation = '20'+str(i)
        # p1 = PersonInfo(name=uname, pid=u_pid, birth=u_birth, birth_address=u_birth_address,
        #                 age=u_age, gender=u_gender,
        #                 address=u_address, phone=u_phone,
        #                 identity=u_identity, relation=u_relation)
        # p1.owner = user
        # p1.save()
    print_line("success")
    return index(request)


def test2(request):
    return index(request)


def add_record(request):
    if request.method == "POST":
        p_name = request.POST.get('person_name')
        p_id = request.POST.get('person_id')
        p_gender = request.POST.get('person_gender')
        p_identity = request.POST.get('person_identity')
        p_birth = request.POST.get('person_birth')
        p_company = request.POST.get('person_company')
        p_phone = request.POST.get('person_phone')
        p_age = request.POST.get('person_age')
        p_birth_address = request.POST.get('person_birth_address')
        p_address = request.POST.get('person_address')
        p_relation = request.POST.get('person_relation')
        p_hobby = request.POST.get('person_hobby')
        p_personality = request.POST.get('person_personality')
        p_correlation_degress = request.POST.get('person_correlation_degree')
        p_notes = request.POST.get('person_notes')
        try:
            if p_name == '':
                raise CustomError("姓名不能为空")

            system_user_name = request.session.get('username')
            print_line("system_user_name")
            print(system_user_name)
            system_user = get_user_model()
            user = system_user.objects.get(username=system_user_name)

            person_info = PersonInfo(name=p_name,
                                     identity=p_identity,
                                     pid=p_id,
                                     address=p_address,
                                     gender=p_gender,
                                     birth=p_birth,
                                     birth_address=p_birth_address,
                                     company=p_company, phone=p_phone,
                                     age=p_age,
                                     relation=p_relation,
                                     hobby=p_hobby,
                                     personality=p_personality,
                                     correlation_degree=p_correlation_degress,
                                     notes=p_notes)

            person_info.owner = user
            person_info.save()
            request.session['info'] = "添加记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    # return index(request)
    return redirect("/PersonManage/index/")


def delete_record(request, personid):
    try:
        person_info = PersonInfo.objects.get(pk=personid)

        person_info.delete()
        # 处理结果，如果需要的话
        request.session['info'] = "记录【" + str(personid) + "】删除成功"
        request.session['success'] = 1
    except Exception as e:
        # 捕获其他类型的异常
        request.session['error'] = str(e)
        request.session['success'] = 0
    return redirect("/PersonManage/index/")


def edit_record(request, personid):
    if request.method == "POST":
        p_name = request.POST.get('person_name')
        p_id = request.POST.get('person_id')
        p_gender = request.POST.get('person_gender')
        p_identity = request.POST.get('person_identity')
        p_birth = request.POST.get('person_birth')
        p_company = request.POST.get('person_company')
        p_phone = request.POST.get('person_phone')
        p_age = request.POST.get('person_age')
        p_birth_address = request.POST.get('person_birth_address')
        p_address = request.POST.get('person_address')
        p_relation = request.POST.get('person_relation')
        p_hobby = request.POST.get('person_hobby')
        p_personality = request.POST.get('person_personality')
        p_correlation_degress = request.POST.get('person_correlation_degree')
        p_notes = request.POST.get('person_notes')
        try:
            if p_name == '':
                raise CustomError("姓名不能为空")
            person_info = PersonInfo.objects.get(pk=personid)
            person_info.name = p_name
            person_info.pid = p_id
            person_info.gender = p_gender
            person_info.identity = p_identity
            person_info.birth = p_birth
            person_info.company = p_company
            person_info.phone = p_phone
            person_info.age = p_age
            person_info.birth_address = p_birth_address
            person_info.address = p_address
            person_info.personality = p_personality
            person_info.correlation_degree = p_correlation_degress
            person_info.relation = p_relation
            person_info.hobby = p_hobby
            person_info.notes = p_notes
            person_info.save()
            request.session['info'] = "修改记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    return redirect("/PersonManage/index/")


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
    person_info = user.owner.all().order_by('-id')
    if request.method == "POST":
        search_content = request.POST.get('searchname')
        person_info = person_info.filter(name__icontains=search_content).order_by('-id')

    # 分页
    p = Paginator(person_info, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "person/index.html", context)
