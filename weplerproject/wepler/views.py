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
    special = "!@#$%&_="
    if request.method =='POST':
        data = json.loads(request.body)
        if len(data['plus_password']) > 7:
            if re.search(r'\d', data['plus_password']):
                if re.search(r'\D', data['plus_password']):
                    if any(s in special for s in data['plus_password']):
                        password = data['plus_password'].encode('utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
                        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
                        password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
                        user_day = data['plus_start_day']
                        user_class = data['plus_fields']
                        u_class = ''
                        p_class = []
                        u_day = ''
                        p_day =[]

                        if data['plus_address_big'] == "seoul" : address = "서울"
                        elif data['plus_address_big'] == "gyeonggi" : address = "경기도"
                        elif data['plus_address_big'] == "incheon" : address = "인천"
                        elif data['plus_address_big'] == "gangwon" : address = "강원도"
                        elif data['plus_address_big'] == "chungbuk" : address = "충청북도"
                        elif data['plus_address_big'] == "chungnam" : address = "충청남도"
                        elif data['plus_address_big'] == "daejeon" : address = "대전"
                        elif data['plus_address_big'] == "jeonbuk" : address = "전라북도"
                        elif data['plus_address_big'] == "jeonnam" : address = "전라남도"
                        elif data['plus_address_big'] == "gwangju" : address = "광주"
                        elif data['plus_address_big'] == "gyeongbuk" : address = "경상북도"
                        elif data['plus_address_big'] == "daegu" : address = "대구"
                        elif data['plus_address_big'] == "gyeongnam" : address = "경상남도"
                        elif data['plus_address_big'] == "ulsan" : address = "울산"
                        elif data['plus_address_big'] == "busan" : address = "부산"
                        else : address = "제주"

                        for i in range(len(user_class)):
                            if user_class[i] == 'education':
                                h_class = '교육'
                            elif user_class[i] == 'council':
                                h_class = '상담'
                            elif user_class[i] == 'making':
                                h_class = '메이킹'
                            elif user_class[i] == 'activity':
                                h_class = '야외활동'
                            elif user_class[i] == 'culture':
                                h_class = '문화'
                            elif user_class[i] == 'trip':
                                h_class = '여행'
                            else:
                                h_class = '기타'
                            u_class = u_class + h_class + ' '
                            p_class.append(h_class)
                        for j in range(len(user_day)):
                            if user_day[j] == 'monday':
                                h_day = '월요일'
                            elif user_day[j] == 'tuesday':
                                h_day = '화요일'
                            elif user_day[j] == 'wednesday':
                                h_day = '수요일'
                            elif user_day[j] == 'thursday':
                                h_day = '목요일'
                            elif user_day[j] == 'friday':
                                h_day = '금요일'
                            elif user_day[j] == 'saturday':
                                h_day = '토요일'
                            else:
                                h_day = '일요일'
                            u_day = u_day + h_day + ' '
                            p_day.append(h_day)
                        p_user = Plus.objects.create(
                            plus_id = data['plus_email'],
                            plus_name = data['plus_name'],
                            plus_password = password_crypt,
                            plus_address_small = data['plus_address_small'],
                            plus_address_big = address,
                            plus_phonenumber = data['plus_phonenumber'],
                            plus_edu = False,
                            plus_talentshare = data['plus_talentshare'],
                            plus_start_time = data['plus_start_time'],
                            plus_end_time = data['plus_end_time'],
                            plus_continu_month = data['plus_continu_month'],
                            plus_point = 0,
                            plus_class = u_class,
                            plus_date = u_day,
                            plus_info = data['plus_oneself'],
                        )
                        Choice_board.objects.create(
                            plus_user = p_user,
                            plus_name = data['plus_name'],
                            plus_address_small = data['plus_address_small'],
                            plus_address_big = data['plus_address_big'],
                            plus_phonenumber = data['plus_phonenumber'],
                            plus_start_time = data['plus_start_time'],
                            plus_end_time = data['plus_end_time'],
                            plus_continu_month = data['plus_continu_month'],
                            plus_point = 0,
                            plus_class = u_class,
                            plus_date = u_day,
                            plus_info = data['plus_oneself'],
                            plus_edu = False,
                        )
                        for k in range(len(p_class)):
                            Plus_field.objects.create(
                                plus_user=p_user,
                                plus_class=p_class[k],
                            )
                        for h in range(len(p_day)):
                            Plus_day.objects.create(
                                plus_user=p_user,
                                plus_date=p_day[h],
                            )
                        return JsonResponse({"len" : True, "hasnumber" : True, "hascharacter" : True, "hasspecial" : True}, status=200)
                    else:
                        return JsonResponse({"len" : True, "hasnumber" : True, "hascharacter" : True, "hasspecial" : False}, status=200)
                else:
                    return JsonResponse({"len" : True, "hasnumber" : True, "hascharacter" : False}, status=200)
            else:
                return JsonResponse({"len" : True, "hasnumber" : False}, status=200)
        else:
            return JsonResponse({"len" : False}, status=200)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def plz_signup(request):
    special = "!@#$%&_="
    if request.method =='POST':
        data = json.loads(request.body)
        if len(data['plz_password']) > 7:
            if re.search(r'\d', data['plz_password']):
                if re.search(r'\D', data['plz_password']):
                    if any(s in special for s in data['plz_password']):
                        password = data['plz_password'].encode('utf-8')             # 입력된 패스워드를 바이트 형태로 인코딩
                        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
                        password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
                        user_class = data['plz_fields']

                        if data['plz_belong'] == {'individual': True}: user_belong = '개인'
                        else: user_belong = '단체'
    
                        if data['plz_address_big'] == "seoul" : address = "서울"
                        elif data['plz_address_big'] == "gyeonggi" : address = "경기도"
                        elif data['plz_address_big'] == "incheon" : address = "인천"
                        elif data['plz_address_big'] == "gangwon" : address = "강원도"
                        elif data['plz_address_big'] == "chungbuk" : address = "충청북도"
                        elif data['plz_address_big'] == "chungnam" : address = "충청남도"
                        elif data['plz_address_big'] == "daejeon" : address = "대전"
                        elif data['plz_address_big'] == "jeonbuk" : address = "전라북도"
                        elif data['plz_address_big'] == "jeonnam" : address = "전라남도"
                        elif data['plz_address_big'] == "gwangju" : address = "광주"
                        elif data['plz_address_big'] == "gyeongbuk" : address = "경상북도"
                        elif data['plz_address_big'] == "daegu" : address = "대구"
                        elif data['plz_address_big'] == "gyeongnam" : address = "경상남도"
                        elif data['plz_address_big'] == "ulsan" : address = "울산"
                        elif data['plz_address_big'] == "busan" : address = "부산"
                        else : address = "제주"

                        if data['plz_when_learn'] == {'specific': True}: user_when = '특별한 날'
                        elif data['plz_when_learn'] == {'regularly': True}: user_when = '정기적으로'
                        else: user_when = '생각중'
                        u_class = ''
                        p_class=[]
                        for i in range(len(user_class)):
                            if user_class[i] == 'education':
                                h_class = '교육'
                                p_class.append(h_class)
                            elif user_class[i] == 'council':
                                h_class = '상담'
                                p_class.append(h_class)
                            elif user_class[i] == 'making':
                                h_class = '메이킹'
                                p_class.append(h_class)
                            elif user_class[i] == 'activity':
                                h_class = '야외활동'
                                p_class.append(h_class)
                            elif user_class[i] == 'culture':
                                h_class = '문화'
                                p_class.append(h_class)
                            elif user_class[i] == 'trip':
                                h_class = '여행'
                                p_class.append(h_class)
                            elif user_class[i] == 'etc':
                                h_class = '기타'
                                p_class.append(h_class)
                            else:
                                h_class = ''
                            u_class = u_class + h_class + ' '
        
                        p_user = Plz.objects.create(
                            plz_id = data['plz_email'],
                            plz_name = data['plz_name'],
                            plz_password = password_crypt,
                            plz_address_big = address,
                            plz_address_small = data['plz_address_small'],
                            plz_when_learn = user_when,
                            plz_phonenumber = data['plz_phonenumber'],
                            plz_group = user_belong,
                            plz_class = u_class,
                        )
                        for k in range(len(p_class)):
                            Plz_field.objects.create(
                                plz_user=p_user,
                                plz_class=p_class[k],
                            )
                        return JsonResponse({"len" : True, "hasnumber" : True, "hascharacter" : True, "hasspecial" : True}, status=200)
                    else:
                        return JsonResponse({"len" : True, "hasnumber" : True, "hascharacter" : True, "hasspecial" : False}, status=200)
                else:
                    return JsonResponse({"len" : True, "hasnumber" : True, "hascharacter" : False}, status=200)
            else:
                return JsonResponse({"len" : True, "hasnumber" : False}, status=200)
        else:
            return JsonResponse({"len" : False}, status=200)
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
                return JsonResponse({"bug" : True}, status=200)
        elif Plus.objects.filter(plus_id = user_id).exists():
            u_id = "plus"
            user = Plus.objects.get(plus_id = user_id)                                                            #입력된 id가 존재하면, 그 id를 가진 plz를 user라는 변수에 넣었음
            if bcrypt.checkpw(user_password, user.plus_password.encode('utf-8')) :                                 #입력된 비밀번호와 변수 user(입력된 id를 가진 plz)의 비밀번호를 비교
                token = jwt.encode({'user_id' : user.plus_id}, SECRET_KEY, algorithm = "HS256")
                token = token.decode('utf-8')                                                                           # 유니코드 문자열로 디코딩
                return JsonResponse({"token" : token, "user_id" : u_id }, status=200)
            else:
                return JsonResponse({"bug" : True}, status=200)
        else:
            return JsonResponse({"bug" : True}, status=200)
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
