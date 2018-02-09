from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    # return HttpResponse('Hello, Django!')
    return render(request, 'index.html')

#登陆请求方法
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:  #username == 'admin' and password =='admin123':
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user', username, 3600) #给浏览器添加cookie
            request.session['user'] = username   #将session的值存入到浏览器
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error'})

#登陆成功后页面
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '') #读取浏览器cookie
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username, 'events':event_list})

#发布会名称查询
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {'user': username, 'events':event_list})

#嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return  render(request, 'guest_manage.html', {'user': username, 'guests':contacts})

#签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})

#签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone','')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': '电话号码不存在.'})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': '发布会活动或者手机号错误.'})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': '已经签到.'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': '签到成功!',
                                                   'guest': result})

#退出系统
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response

















































