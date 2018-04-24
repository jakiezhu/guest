#!/usr/bin/python
# coding=utf-8
from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import time


# 添加发布会接口
def add_event(request):
    eid = request.POST.get('eid', '')       # 发布会id
    name = request.POST.get('name', '')       # 发布会标题
    limit = request.POST.get('limit', '')       # 发布会限制人数
    status = request.POST.get('status', '')       # 发布会状态
    address = request.POST.get('address', '')       # 发布会地址
    start_time = request.POST.get('start_time', '')       # 发布会时间

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': '参数错误'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': '发布会ID已经存在'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': '发布会名称已经存在'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address,
                             status=int(status), start_time=start_time)
    except ValidationError as e:
        error = '开始时间格式错误，正确格式为：YYYY-MM-DD HH:MM:SS'
        return JsonResponse({'status': 10024, 'message': error})

    return JsonResponse({'status': 200, 'message': '添加成功'})


# 添加嘉宾接口
def add_guest(request):
    eid = request.POST.get('eid', '')       # 发布会id
    realname = request.POST.get('name', '')       # 姓名
    phone = request.POST.get('limit', '')       # 手机号
    email = request.POST.get('status', '')       # 邮箱

    if eid == '' or realname == '' or phone == '' or email == '':
        return JsonResponse({'status': 10021, 'message': '参数错误'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': '发布会ID不存在'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': '发布会不可用'})

    event_limit = Event.objects.get(id=eid).limit
    guests_all = Guest.objects.filter(event_id=eid)

    if len(guests_all) >= event_limit:
        return JsonResponse({'status': 10024, 'message': '发布会人数已满'})

    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message': '发布会已经开始了'})

    try:
        Event.objects.create(event_id=int(eid), realname=realname, phone=int(phone), email=email,
                             sign=0)
    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': '发布会嘉宾号码重复'})

    return JsonResponse({'status': 200, 'message': '添加成功'})