from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import bcrypt                          # 암호화에 사용
import jwt                             # 토큰 발행에 사용
import re

@csrf_exempt
def plus_signup(request):
    if request.method =='POST':
        data = json.loads(request.body)
        password = data['plus_password'].encode('utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
        user_day = data['plus_start_day']
        user_class = data['plus_fields']
        p_user = Plus.objects.create(
            plus_id = data['plus_email'],
            plus_name = data['plus_name'],
            plus_password = password_crypt,
            plus_address_small = data['plus_address_small'],
            plus_address_big = data['plus_address_big'],
            plus_phonenumber = data['plus_phonenumber'],
            plus_edu = False,
            plus_talentshare = data['plus_talentshare'],
            plus_start_time = data['plus_start_time'],
            plus_end_time = data['plus_end_time'],
            plus_continu_month = data['plus_continu_month'],
            plus_point = 0,
        )
        for i in range(len(user_class)):
            if user_class[i].class_name == 'education':
                h_class = '교육'
            elif user_class[i].class_name == 'council':
                h_class = '상담'
            elif user_class[i].class_name == 'making':
                h_class = '메이킹'
            elif user_class[i].class_name == 'activity':
                h_class = '야외활동'
            elif user_class[i].class_name == 'culture':
                h_class = '문화'
            elif user_class[i].class_name == 'trip':
                h_class = '여행'
            else:
                h_class = '기타'
            u_class = u_class + h_class + ' '
        Plus_class.objects.create(
            plz_user = p_user,
            class_name = u_class,
        )
        u_day = ''
        for j in range(len(user_day)):
            if user_class[j].class_name == 'monday':
                h_day = '월요일'
            elif user_class[j].class_name == 'tuesday':
                h_day = '화요일'
            elif user_class[j].class_name == 'wednesday':
                h_day = '수요일'
            elif user_class[j].class_name == 'thursday':
                h_day = '목요일'
            elif user_class[j].class_name == 'friday':
                h_day = '금요일'
            elif user_class[j].class_name == 'saturday':
                h_day = '토요일'
            else:
                h_day = '일요일'
            u_day = u_day + h_day + ' '
        Plus_date.objects.create(
            plus_user=p_user
            plus_start_day=u_day
        )
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def plz_signup(request):
    special = "!@#$%&_="
    if request.method =='POST':
        data = json.loads(request.body)
        if re.search(r'\d', data['plz_password']):
            if re.search(r'\D', data['plz_password']):
                if any(s in special for s in data['plz_password']):
                    password = data['plz_password'].encode('utf-8')             # 입력된 패스워드를 바이트 형태로 인코딩
                    password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
                    password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
                    user_class = data['plz_fields']

                    if data['plz_belong'] == {'individual': True}: user_belong = 'individual'
                    else: user_belong = 'group'
                    
                    if data['plz_when_learn'] == {'specific': True}: user_when = 'specific'
                    elif data['plz_when_learn'] == {'regularly': True}: user_when = 'regularly'
                    else: user_when = 'thinking'
                        
                    print(data['plz_phonenumber']) 
                    p_user = Plz.objects.create(
                        plz_id = data['plz_email'],
                        plz_name = data['plz_name'],
                        plz_password = password_crypt,
                        plz_address_big = data['plz_address_big'],
                        plz_address_small = data['plz_address_small'],
                        plz_when_learn = data['plz_when_learn'],
                        plz_phonenumber = data['plz_phonenumber'],
                        plz_group = user_belong,
                    )
                    u_class = ''
                    for i in range(len(user_class)):
                        if user_class[i].class_name == 'education':
                            h_class = '교육'
                        elif user_class[i].class_name == 'council':
                            h_class = '상담'
                        elif user_class[i].class_name == 'making':
                            h_class = '메이킹'
                        elif user_class[i].class_name == 'activity':
                            h_class = '야외활동'
                        elif user_class[i].class_name == 'culture':
                            h_class = '문화'
                        elif user_class[i].class_name == 'trip':
                            h_class = '여행'
                        else:
                            h_class = '기타'
                        u_class = u_class + h_class + ' '
                    Plz_class.objects.create(
                        plz_user = user_info,
                        class_name = u_class,
                    )
                    return JsonResponse({"hasnumber" : True, "hascharacter" : True, "hasspecial" : True}, status=200)
                else:
                    return JsonResponse({"hasnumber" : True, "hascharacter" : True, "hasspecial" : False}, status=200)
            else:
                return JsonResponse({"hasnumber" : True, "hascharacter" : False}, status=200)
        else:
            return JsonResponse({"hasnumber" : False}, status=200)
    else:
            return HttpResponse(status=400)

@csrf_exempt
def login(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method =='POST':
        data = json.loads(request.body)
        user_id = data['email']
        user_password = data['password'].encode('utf-8')   
        if Plz.objects.filter(plz_id = user_id).exists():
            u_id = "plz"
            user = Plz.objects.get(plz_id = user_id)                                                            #입력된 id가 존재하면, 그 id를 가진 plz를 user라는 변수에 넣었음
            if bcrypt.checkpw(user_password, user.plz_password.encode('utf-8')) :                                 #입력된 비밀번호와 변수 user(입력된 id를 가진 plz)의 비밀번호를 비교
                token = jwt.encode({'user_id' : user.plz_id}, SECRET_KEY, algorithm = "HS256").decode('utf-8')   # 유니코드 문자열로 디코딩                                                                      
                return JsonResponse({"token" : token, "user_id" : u_id }, status=200)
            else:
                return HttpResponse(status=401)
        elif Plus.objects.filter(plus_id = user_id).exists():
            u_id = "plus"
            user = Plus.objects.get(plus_id = user_id)                                                            #입력된 id가 존재하면, 그 id를 가진 plz를 user라는 변수에 넣었음
            if bcrypt.checkpw(user_password, user.plus_password.encode('utf-8')) :                                 #입력된 비밀번호와 변수 user(입력된 id를 가진 plz)의 비밀번호를 비교
                token = jwt.encode({'user_id' : user.plus_id}, SECRET_KEY, algorithm = "HS256")
                token = token.decode('utf-8')                                                                           # 유니코드 문자열로 디코딩
                return JsonResponse({"token" : token, "user_id" : u_id }, status=200)
            else:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)

def id_check(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        user_id = data['email']
        if Plus.objects.filter(plus_id=user_id).exists or Plz.objects.filter(plz_id=user_id).exists:
            return JsonResponse({"isoverap" : True}, status=200)
        else: JsonResponse({"isoverap" : False}, status=200)
    else: HttpResponse(status=400)

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'GET':
        token = request.headers.get('Authorization', None)
        user_token_info = jwt.decode(token, SECRET_KEY, algorithm = "HS256")
        if Plus.objects.filter(plus_id=user_token_info['user_id']).exists() :
            return JsonResponse({"user_email" : user_token_info['user_id']}, status=200)
        elif Plz.objects.filter(plz_id=user_token_info['user_id']).exists() :
            return JsonResponse({"user_email" : user_token_info['user_id']}, status=200)
        return HttpResponse(status=403)
    else:
        HttpResponse(status=400)
