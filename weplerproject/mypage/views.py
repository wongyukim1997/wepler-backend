from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status 
from wepler.models import *
from wepler.serializers import *
import jwt                             # 토큰 발행에 사용
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_exempt

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
            user_day_count = Plus_date.objects.filter(plus_user = user_id)
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
            user_group = user_info.plz_group
            user_when_learn = user_info.plz_when_learn
            user_class_count = Plz_class.objects.filter(plz_user_id = user_id)
            user_class = []
            for i in range(user_class_count.count()):
                user_class.append(user_class_count[i].class_name)
            return JsonResponse({"user_name" : user_name, "user_phone" : user_phone, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_group" : user_group, "user_when_learn" : user_when_learn, "user_class" : user_class, "user_email" : user_id}, status=200)
        else:
            return HttpResponse(staus = 403)
    else:
        return HttpResponse(staus = 400)

@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = tokenCheck(request)
        if Plus.objects.filter(plus_id=user_id).exists() :
            user_info = Plus.objects.filter(plus_id=user_id)[0]
            user_field = Plus_class.objects.filter(plus_user=user_id)
            user_field.delete()
            #user_info.plus_start_day = data['plus_start_day']       #이게 뭔지 모르겠음
            user_info.plus_talentshare = data['plus_talentshare']
            user_info.plus_continu_month = data['plus_continu_month']
            user_info.plus_start_time = data['plus_start_time']
            user_info.plus_end_time = data['plus_end_time']
            user_class = data['plus_fields']
            for i in range(len(user_class)):
                Plus_class.objects.create(
                    plus_user = user_info,
                    class_name = user_class[i],
                )
            return HttpResponse(status=200)
        elif Plus.objects.filter(plus_id=user_id).exists() :
            user_info = Plz.objects.filter(plz_id=user_id)[0]
            user_field = Plz_class.objects.filter(plz_user=user_id)
            user_field.delete()
            #plz 어떤 정보 수정인지 알아보기
            user_class = data['plus_fields']
            for i in range(len(user_class)):
                Plz_class.objects.create(
                    plz_user = user_info,
                    class_name = user_class[i],
                )
            return HttpResponse(status=200)
        else: return HttpResponse(status=400)
    else: return HttpResponse(status=403)

class Apply_list(viewsets.ModelViewSet):
    queryset = Plus_apply.objects.all()
    serializer_class = Plus_ApplySerializer

#Plus가 신청한걸 Plz가 거절하는 경우
@csrf_exempt
def apply_delete(request, apply_id):
    if request.method == 'DELETE':
        pa = Plus_apply.objects.filter(id=apply_id)[0]
        pa.delete()
        return HttpResponse(status = 200)
    else: return HttpResponse(status=400)

#수락한 경우
@csrf_exempt
def user_match(request, apply_id): #아직 어떤 정보를 띄우는게 좋은지 모른다.
    if request.method == 'POST':
        user_id = tokenCheck(request)
        h_id = Plus_apply.objects.filter(id=apply_id)[0].hire_id
        p_id = Plus_apply.objects.filter(id=apply_id)[0].plus_user
        if Plz.objects.filter(plz_id = user_id).exists():
            Match.objects.create(
                plz_user = Plz.objects.filter(plz_id = user_id)[0],
                plus_user = Plus.objects.filter(plus_id = p_id)[0],
                match_subject = Hire_board.objects.filter(id=h_id).title,
                complete = False,
            )
            apply = Plus_apply.objects.filter(id=apply_id)
            apply.delete()
            return HttpResponse(status=200)
        else: return HttpResponse(status=400)
    else: return HttpResponse(status=403)

def apply_detail(request, apply_id):        #이부분은 소현이가 원하는 데이터 넘겨주면 됨
    if request.method == 'GET':
        apply = Plus_apply.objects.filter(id = apply_id)[0]
        user_id = apply.plus_user_id
        p_user = Plus.objects.filter(plus_id = user_id)[0]
        
        user_id = apply.plus_user_id
        user_name = apply.plus_user_name
        user_class = apply.plus_class
        user_day = apply.plus_date
        user_phone = p_user.plus_phonenumber
        user_address_big = p_user.plus_address_big
        user_address_small = p_user.plus_address_small
        user_month = p_user.plus_continu_month
        user_start = p_user.plus_start_time
        user_end = p_user.plus_end_time
        user_talent = p_user.plus_talentshare
        user_point = p_user.plus_point
        return JsonResponse({"user_name" : user_name, "user_day" : user_day, "user_start" : user_start, "user_end" : user_end, "user_phone" : user_phone, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_class" : user_class, "user_email" : user_id, "user_point" : user_point}, status=200)
    else: return HttpResponse(status=400)

#진행중인 봉사
class Match_list(viewsets.ModelViewSet):
    queryset = Match.objects.filter(complete=False)
    serializer_class = MatchSerializer
#완료된 봉사, plz에서 볼 것
class Plz_match_complete_list(viewsets.ModelViewSet):
    queryset = Match.objects.filter(complete=True).distinct('plus_user')
    serializer_class = MatchSerializer
#완료된 봉사, plus에서 볼 것
class Plus_match_complete_list(viewsets.ModelViewSet):
    queryset = Match.objects.filter(complete=True).distinct('plz_user')
    serializer_class = MatchSerializer

@csrf_exempt
def match_complete(request, match_id):
    if request.method == 'POST':
        ma = Match.objects.filter(id = match_id)[0]
        ma.complete = True
        ma.save()
        return HttpResponse(status=200)
    else: return HttpResponse(status=400)
