from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, status 
from wepler.models import *
from wepler.serializers import *
import jwt                             # 토큰 발행에 사용
from django.views.decorators.csrf import csrf_exempt
import json

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'GET' or request.method == 'POST':
        token = request.headers.get('Authorization', None)
        print(token)
        user_token_info = jwt.decode(token, SECRET_KEY, algorithm = "HS256")
        if Plus.objects.filter(plus_id=user_token_info['user_id']).exists() :
            user_id = user_token_info['user_id']
            return user_id
        elif Plz.objects.filter(plz_id=user_token_info['user_id']).exists() :
            user_id = user_token_info['user_id']
            return user_id 
        return HttpResponse(status=403)
    else:
        HttpResponse(status=400)

def plus_profile_list(reuqest, address):
    if reuqest.method == 'GET':
        qs = Choice_board.objects.filter(plus_address_big=address)
        serializer = Choice_boardSerializer(qs, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    else: return HttpResponse(status=400)

def plus_profile_list_count(request, address):
    if request.method == 'GET':
        count = Choice_board.objects.filter(plus_address_big=address).count()
        return JsonResponse({"count" : count }, status=200)
    else: return HttpResponse(status=400)

def plus_profile_detail(request, choice_id):
    if request.method == 'GET':
        choice = Choice_board.objects.filter(id=choice_id)[0]  
        fields = choice.plus_class
        day = choice.plus_date
        cont = choice.plus_continu_month
        start = choice.plus_start_time
        end = choice.plus_end_time
        name = choice.plus_name
        email = choice.plus_user_id
        point = choice.plus_point
        info = choice.plus_info
        if choice.plus_edu == 0: edu = 'X'
        else : edu = 'O'
        return JsonResponse({"plus_point" : point, "plus_info" : info, "plus_fields" : fields, "plus_start_day" : day, "plus_continu_month" : cont, "plus_start_time" : start, "plus_end_time" : end, "plus_name" : name, "plus_id" : email, "plus_edu" : edu}, status=200)
    else: return HttpResponse(status=400)

@csrf_exempt
def apply(request, choice_id):
    if request.method == 'POST':
        user_id = tokenCheck(request)
        choice = Choice_board.objects.filter(id=choice_id)[0]
        plus = Plus.objects.filter(plus_id=choice.plus_user_id)
        plz = Plz.objects.filter(plz_id=user_id)
        if Plz_apply.objects.filter(choice_id=choice_id).filter(plz_user_id=plz[0].plz_id).exists(): #여기서 choice_id로 바꿔서 해결해야함
            return JsonResponse({"isoverap" : True}, status=200)
        else:
            Plz_apply.objects.create(
                plus_user = plus[0],
                plz_user = plz[0],
                plus_class = plus[0].plus_class,
                plz_class = plz[0].plz_class,
                plz_user_name = plz[0].plz_name,
                plus_user_name = plus[0].plus_name,
                plus_address = plus[0].plus_address_big,
                plz_address = plz[0].plz_address_big,
                plus_date = plus[0].plus_date,
                choice_id=Choice_board.objects.filter(id=choice_id)[0],
                plus_point=plus[0].plus_point,
            )
            return JsonResponse({"isoverap" : False}, status=200)
    else: return HttpResponse(status=400)
