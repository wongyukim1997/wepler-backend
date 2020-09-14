from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from wepler.models import *
from wepler.serializers import *
import jwt                             # 토큰 발행에 사용
from django.views.decorators.csrf import csrf_exempt
import json

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'GET':
        token = request.headers.get('Authorization', None)
        user_token_info = jwt.decode(token, SECRET_KEY, algorithm = "HS256")
        if Plus.objects.filter(plus_id=user_token_info['plus_id']).exists() :
            user_id = user_token_info['plus_id']
            return user_id
        elif Plz.objects.filter(plz_id=user_token_info['plz_id']).exists() :
            user_id = user_token_info['plz_id']
            return user_id 
        return HttpResponse(status=403)
    else:
        HttpResponse(status=400)

def getMypage(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plus.objects.filter(plus_id = user_id).exists():
            user_info = Plus.objects.filter(plus_id = user_id)[0]
            user_name = user_info.plus_name
            user_phone = user_info.plus_phonenumber
            user_address_big = user_info.plus_address_big
            user_address_small = user_info.plus_address_small
            user_month = user_info.plus_continu_month
            user_start = user_info.plus_start_time
            user_end = user_info.plus_end_time
            user_talent = user_info.plus_talentshare
            user_class_count = Plus_class.objects.filter(plus_user_id = user_id)
            user_day_count = Plus_date.objects.filter(plus_user=user_id)
            user_class = []
            user_day = []
            for i in range(user_class_count.count()):
                user_class.append(user_class_count[i].class_name)
            for j in range(user_day_count.count()):
                user_day.append(user_day_count[j].plus_start_day)
            return JsonResponse({"user_name" : user_name, "user_phone" : user_phone, "user_class" : user_class, "user_email" : user_id, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_continu_month" : user_month, "user_start_time" : user_start, "user_end_time" : user_end, "user_talentshare" : user_talent, "user_start_day" : user_day}, status=200)
        elif Plz.objects.filter(plz_id = user_id).exists():
            user_info = Plz.objects.filter(plz_id = user_id)[0]
            user_name = user_info.plz_name
            user_phone = user_info.plz_phonenumber
            user_address_big = user_info.plz_address_big
            user_address_small = user_info.plz_address_small
            user_month = user_info.plz_continu_month
            user_start = user_info.plz_start_time
            user_end = user_info.plz_end_time
            user_talent = user_info.plz_talentshare
            user_class = Plz_class.objects.filter(plz_user_id = user_n)
            print(user_class)
            return JsonResponse({"user_name" : user_name, "user_phone" : user_phone}, status=200)
        else:
            return HttpResponse(staus = 403)
    else:
        return HttpResponse(staus = 400)
