from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import get_user_model
from django.db import IntegrityError
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
    recipe_info = user.recipes_info.all().order_by('-id')
    ingredient_info = Ingredient.objects.all()
    context['ingredients'] = ingredient_info
    # 分页
    p = Paginator(recipe_info, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "cookbook/index.html", context)


def test1(request):
    system_user_name = 'oper'
    system_user = get_user_model()
    user = system_user.objects.get(username=system_user_name)

    # for i in range(0, 10):
    #     uname = "shicai"+str(i)
    #     p1 = Ingredient(name=uname)
    #     # p1.owner = user
    #     p1.save()

    # for i in range(0, 20):
    #     uname = "caipu"+str(i)
    #     step = "jianchao"+str(i)
    #     p1 = Recipe(name=uname, steps=step)
    #     p1.owner = user
    #     p1.save()
    #
    #     ingredient = Ingredient.objects.get(id=2)
    #     p1.ingredients.add(ingredient)
    #     ingredient = Ingredient.objects.get(id=3)
    #     p1.ingredients.add(ingredient)

    print_line("success")
    return index(request)


def test2(request):

    return index(request)


def add_record(request):
    if request.method == "POST":
        cb_name = request.POST.get('cbname')
        cb_ingredients = request.POST.get('cbingredients')
        cb_steps = request.POST.get('cb_steps')
        try:
            if cb_name == '':
                raise CustomError("名称不能为空")
            if cb_ingredients == '':
                raise CustomError("食材不能为空")
            else:
                ingredients = parse_tags(cb_ingredients)
                if len(ingredients) == 0:
                    raise CustomError("食材不能为空")
            system_user_name = request.session.get('username')
            system_user = get_user_model()
            user = system_user.objects.get(username=system_user_name)

            recipe = Recipe(name=cb_name, steps=cb_steps)
            recipe.owner = user
            recipe.save()

            for ingredient in ingredients:
                ing_exists = Ingredient.objects.filter(name=ingredient).exists()
                if not ing_exists:
                    ingredient = Ingredient(name=ingredient)
                    ingredient.save()
                    recipe.ingredients.add(ingredient)
                else:
                    ingredient = Ingredient.objects.get(name=ingredient)
                    recipe.ingredients.add(ingredient)

            request.session['info'] = "添加记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    # return index(request)
    return redirect("/CookbookManage/index/")


def add_ingredient(request):
    if request.method == "POST":
        p_name = request.POST.get('ingname')
        try:
            if p_name == '':
                raise CustomError("名称不能为空")
            else:
                ings = parse_tags(p_name)
                if len(ings) == 0:
                    raise CustomError("名称不能为空")
            for ing in ings:
                ing_exists = Ingredient.objects.filter(name=ing).exists()
                if not ing_exists:
                    ingredient = Ingredient(name=ing)
                    ingredient.save()
            request.session['info'] = "添加记录成功"
            request.session['success'] = 1
        except IntegrityError as e:
            # 捕获其他类型的异常
            request.session['error'] = "食材已存在，请勿重复添加"
            request.session['success'] = 0
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    # return index(request)
    return redirect("/CookbookManage/index/")


def delete_record(request, cbid):
    try:
        recipe = Recipe.objects.get(id=cbid)
        recipe.delete()
        # 处理结果，如果需要的话
        request.session['info'] = "记录【" + str(cbid) + "】删除成功"
        request.session['success'] = 1
    except Exception as e:
        # 捕获其他类型的异常
        request.session['error'] = str(e)
        request.session['success'] = 0
    return redirect("/CookbookManage/index/")


def edit_record(request, cbid):
    if request.method == "POST":
        cb_name = request.POST.get('cbname')
        cb_ingredients = request.POST.get('cbingredients')
        cb_steps = request.POST.get('cb_steps')
        try:
            if cb_name == '':
                raise CustomError("名称不能为空")
            if cb_ingredients == '':
                raise CustomError("食材不能为空")
            else:
                ingredients = parse_tags(cb_ingredients)
                if len(ingredients) == 0:
                    raise CustomError("食材不能为空")

            recipe = Recipe.objects.get(pk=cbid)
            recipe.name = cb_name
            recipe.steps = cb_steps
            recipe.ingredients.clear()
            for ingredient in ingredients:
                ing_exists = Ingredient.objects.filter(name=ingredient).exists()
                if not ing_exists:
                    ingredient = Ingredient(name=ingredient)
                    ingredient.save()
                    recipe.ingredients.add(ingredient)
                else:
                    ingredient = Ingredient.objects.get(name=ingredient)
                    recipe.ingredients.add(ingredient)
            recipe.save()
            request.session['info'] = "修改记录成功"
            request.session['success'] = 1
        except Exception as e:
            # 捕获其他类型的异常
            request.session['error'] = str(e)
            request.session['success'] = 0
    return redirect("/CookbookManage/index/")


def cbsearch(request, context=None):
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
    recipes = user.recipes_info.all().order_by('-id')
    ingredient_info = Ingredient.objects.all()
    context['ingredients'] = ingredient_info
    if request.method == "POST":
        search_content = request.POST.get('cbname')
        recipes = recipes.filter(name__icontains=search_content).order_by('-id')

    # 分页
    p = Paginator(recipes, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj
    return render(request, "cookbook/index.html", context)


def ingsearch(request, context=None):
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
    recipes = user.recipes_info.all().order_by('-id')
    ingredient_info = Ingredient.objects.all()
    context['ingredients'] = ingredient_info
    if request.method == "POST":
        search_content = request.POST.get('ingname')
        ingredients = parse_tags(search_content)
        if search_content != '' and len(ingredients) != 0:
            ingredients_list = Ingredient.objects.filter(name__in=ingredients)
            recipes = recipes.filter(ingredients__in=ingredients_list).distinct()
    # 分页
    p = Paginator(recipes, 9)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        page_obj = p.get_page(page_number)
    except EmptyPage as e:
        # 如果页码无效（例如不是整数、小于 1 或大于总页数），则显示第一页或最后一页
        page_obj = p.get_page(1)

    context['page_obj'] = page_obj

    return render(request, "cookbook/index.html", context)
    # return redirect("/CookbookManage/index/", context)
    # return index(request, context)





