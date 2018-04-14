from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'index.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)
            return response
        else:
            return render(request, 'index.html', {'error': '用户名或密码错误！'})


@login_required
def event_manage(request):
    # username = request.COOKIES.get("user", '')
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


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
    return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})


@login_required
def search_guest(request):
    username = request.session.get('user', '')
    name = request.GET.get('name', '')
    guest_list = Guest.objects.filter(realname__contains=name)
    return render(request, 'guest_manage.html', {'user': username, 'guests': guest_list})


@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    username = request.session.get('user', '')
    guests_num = Guest.objects.filter(event_id=event_id).count()
    sign_guests_num = Guest.objects.filter(event_id=event_id, sign=True).count()
    return render(request, 'sign_index.html', {'user': username, 'event': event,
                                               'guests_num': guests_num, 'sign_guests_num': sign_guests_num})


@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')
    # 统计所有嘉宾数和已签到嘉宾
    guests_num = Guest.objects.filter(event_id=event_id).count()
    sign_guests_num = Guest.objects.filter(event_id=event_id, sign=True).count()

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': '电话号码错误！',
                                               'guests_num': guests_num, 'sign_guests_num': sign_guests_num})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': '发布会ID或电话号码错误！',
                                               'guests_num': guests_num, 'sign_guests_num': sign_guests_num})

    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': '已签到',
                                               'guests_num': guests_num, 'sign_guests_num': sign_guests_num})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        sign_guests_num = sign_guests_num + 1
        return render(request, 'sign_index.html', {'event': event, 'hint': '签到成功！', 'guest': result,
                                               'guests_num': guests_num, 'sign_guests_num': sign_guests_num})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')