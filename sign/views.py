from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
    # username = request.COOKIES.get('user', '') #读取浏览器cookie
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username})
