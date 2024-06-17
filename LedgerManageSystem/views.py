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
    ledger_info = user.ledger_info.all().order_by('-id')
    context['ledger_info'] = ledger_info
    #
    # # 分页
    p = Paginator(ledger_info, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    context['active_page'] = 0
    return render(request, "ledger/index.html", context)


def ledger(request, lid, context=None):
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
    ledger_info_set = user.ledger_info.all().order_by('-id')
    context['ledger_info'] = ledger_info_set

    # 获取账本信息
    try:
        ledger_info = LedgerInfo.objects.get(pk=lid)
        # 获取该账本的所有账目记录
        account_entries = ledger_info.entries.all().order_by('-id')
        context['ledger_name'] = ledger_info.name
        context['ledger_id'] = ledger_info.id
        context['account_num'] = len(account_entries)
        #
        # # 分页
        p = Paginator(account_entries, 10)  # Show 25 contacts per page.
        page_number = request.GET.get("page", 1)
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
        context['page_obj'] = page_obj
    except LedgerInfo.DoesNotExist:
        # 处理账本不存在的情况
        request.session['error'] = "账本不存在"
        request.session['success'] = 0
    # request.session['active_page'] = lid
    context['active_page'] = lid
    return render(request, "ledger/ledger.html", context)


def test1(request):
    system_user_name = 'gaopeng'
    system_user = get_user_model()
    user = system_user.objects.get(username=system_user_name)
    ledger_info = user.ledger_info.all().order_by('-id')
    # for l in ledger_info:
    #     print_line(l.id)
    #     ae = AccountEntry(theoretical_income=0.00,
    #                       theoretical_expenditure=0.00,
    #                       actual_income=0.00,
    #                       actual_expenditure=0.00,
    #                       theoretical_balance=0.00,
    #                       actual_balance=0.00,
    #                       difference=0.00,
    #                       account_book_id=l.id)
    #     ae.save()

    # for i in range(7, 30):
    #     uname = "zhangben"+str(i)
    #     p1 = LedgerInfo(name=uname, notes='alice', owner_id=12)
    #     p1.save()
    print_line("success")
    return index(request)


def test2(request):

    return index(request)


def search_ledger(request, context=None):
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
    ledger_info = user.ledger_info.all().order_by('-id')
    context['ledger_info'] = ledger_info
    if request.method == "POST":
        search_content = request.POST.get('searchname')
        ledger_info = ledger_info.filter(name__icontains=search_content).order_by('-id')
    # 分页
    p = Paginator(ledger_info, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "ledger/index.html", context)


def search_account(request, context=None):
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
    ledger_info = user.ledger_info.all().order_by('-id')
    context['ledger_info'] = ledger_info
    if request.method == "POST":
        search_content = request.POST.get('searchname')
        ledger_info = ledger_info.filter(name__icontains=search_content).order_by('-id')
    # 分页
    p = Paginator(ledger_info, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "ledger/index.html", context)


def add_ledger(request):
    if request.method == "POST":
        l_name = request.POST.get('ledgername')
        l_notes = request.POST.get('notes')
        # print(p_name, p_username, p_password, p_phone_number, p_email, p_website, p_notes, sep='|')
        try:
            if l_name == '':
                raise CustomError("应用名称不能为空")
            system_user_name = request.session.get('username')
            # print_line("system_user_name")
            # print(system_user_name)
            system_user = get_user_model()
            user = system_user.objects.get(username=system_user_name)

            ledger_info = LedgerInfo(name=l_name, notes=l_notes)
            ledger_info.owner = user
            ledger_info.save()
            ae = AccountEntry(theoretical_income=0.00,
                              theoretical_expenditure=0.00,
                              actual_income=0.00,
                              actual_expenditure=0.00,
                              theoretical_balance=0.00,
                              actual_balance=0.00,
                              difference=0.00)
            ae.account_book = ledger_info
            ae.save()
            request.session['info'] = "添加记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    # return index(request)
    return redirect("/LedgerManage/index/")


def add_account(request, lid):
    if request.method == "POST":
        a_theoretical_income = request.POST.get('theoretical_income')
        a_actual_income = request.POST.get('actual_income')
        a_theoretical_expenditure = request.POST.get('theoretical_expenditure')
        a_actual_expenditure = request.POST.get('actual_expenditure')
        a_remark = request.POST.get('remark')
        # print(p_name, p_username, p_password, p_phone_number, p_email, p_website, p_notes, sep='|')
        try:
            a_theoretical_income = format_decimal_string(a_theoretical_income)
            a_actual_income = format_decimal_string(a_actual_income)
            a_theoretical_expenditure = format_decimal_string(a_theoretical_expenditure)
            a_actual_expenditure = format_decimal_string(a_actual_expenditure)
            # 获取最后一条记录
            last_entry = AccountEntry.objects.filter(account_book_id=lid).order_by('-created_at').first()
            a_theoretical_balance = last_entry.theoretical_balance + a_theoretical_income - a_theoretical_expenditure
            a_actual_balance = last_entry.actual_balance + a_actual_income - a_actual_expenditure
            a_difference = a_actual_balance - a_theoretical_balance
            ledger_info = LedgerInfo.objects.get(pk=lid)
            ae = AccountEntry(theoretical_income=a_theoretical_income,
                              theoretical_expenditure=a_theoretical_expenditure,
                              actual_income=a_actual_income,
                              actual_expenditure=a_actual_expenditure,
                              theoretical_balance=a_theoretical_balance,
                              actual_balance=a_actual_balance,
                              difference=a_difference,
                              remark=a_remark)
            ae.account_book = ledger_info
            ae.save()
            request.session['info'] = "添加记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    # return index(request)
    return redirect("/LedgerManage/ledger/"+str(lid))


def edit_ledger(request, pid):
    if request.method == "POST":
        l_name = request.POST.get('ledgername')
        l_notes = request.POST.get('notes')
        try:
            if l_name == '':
                raise CustomError("应用名称不能为空")
            ledger_info = LedgerInfo.objects.get(pk=pid)
            ledger_info.name = l_name
            ledger_info.notes = l_notes
            ledger_info.save()
            request.session['info'] = "修改记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    return redirect("/LedgerManage/index/")


def edit_account(request, lid, aid):
    if request.method == "POST":
        a_theoretical_income = request.POST.get('theoretical_income')
        a_actual_income = request.POST.get('actual_income')
        a_theoretical_expenditure = request.POST.get('theoretical_expenditure')
        a_actual_expenditure = request.POST.get('actual_expenditure')
        a_remark = request.POST.get('remark')
        try:
            a_theoretical_income = format_decimal_string(a_theoretical_income)
            a_actual_income = format_decimal_string(a_actual_income)
            a_theoretical_expenditure = format_decimal_string(a_theoretical_expenditure)
            a_actual_expenditure = format_decimal_string(a_actual_expenditure)
            aid_account_info = AccountEntry.objects.get(account_book_id=lid, id=aid)
            gap_theoretical_income = a_theoretical_income - aid_account_info.theoretical_income
            gap_actual_income = a_actual_income - aid_account_info.actual_income
            gap_theoretical_expenditure = a_theoretical_expenditure - aid_account_info.theoretical_expenditure
            gap_actual_expenditure = a_actual_expenditure - aid_account_info.actual_expenditure

            gap_difference = (gap_actual_income - gap_actual_expenditure -
                              gap_theoretical_income + gap_theoretical_expenditure)
            gap_theoretical = gap_theoretical_income - gap_theoretical_expenditure
            gap_actual = gap_actual_income - gap_actual_expenditure

            aid_account_info.theoretical_balance = (aid_account_info.theoretical_balance + gap_theoretical)
            aid_account_info.actual_balance = (aid_account_info.actual_balance + gap_actual)
            aid_account_info.difference = (aid_account_info.difference + gap_difference)
            aid_account_info.theoretical_income = a_theoretical_income
            aid_account_info.actual_income = a_actual_income
            aid_account_info.theoretical_expenditure = a_theoretical_expenditure
            aid_account_info.actual_expenditure = a_actual_expenditure
            aid_account_info.remark = a_remark
            aid_account_info.save()

            # 获取所有记录
            all_account_info = AccountEntry.objects.filter(account_book_id=lid).order_by('-id')
            # 获取所有id > aid 的记录，，不包括aid
            edit_account_info = all_account_info.filter(id__gt=aid)
            print_line(aid)
            for obj in edit_account_info:
                obj.theoretical_balance = obj.theoretical_balance + gap_theoretical
                obj.actual_balance = obj.actual_balance + gap_actual
                obj.difference = obj.difference + gap_difference
                obj.save()
            request.session['info'] = "修改记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    return redirect("/LedgerManage/ledger/" + str(lid))


def delete_ledger(request, pid):
    try:
        ledger_info = LedgerInfo.objects.get(pk=pid)
        ledger_info.delete()
        # 处理结果，如果需要的话
        request.session['info'] = "记录【" + str(pid) + "】删除成功"
        request.session['success'] = 1
    except Exception as e:
        # 捕获其他类型的异常
        request.session['error'] = str(e)
        request.session['success'] = 0
    return redirect("/LedgerManage/index/")


def delete_account(request, lid, aid):
    try:
        entry_count = AccountEntry.objects.filter(account_book_id=lid).count()
        if entry_count <= 1:
            raise CustomError("删除失败！！\n账目记录至少要保持一条！！")

        account_info = AccountEntry.objects.get(pk=aid)
        account_info.delete()
        # 处理结果，如果需要的话
        request.session['info'] = "记录【" + str(aid) + "】删除成功"
        request.session['success'] = 1
    except Exception as e:
        # 捕获其他类型的异常
        request.session['error'] = str(e)
        request.session['success'] = 0
    return redirect("/LedgerManage/ledger/"+str(lid))
