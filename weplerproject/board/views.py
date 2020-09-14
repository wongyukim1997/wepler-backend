from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from wepler.models import *
from wepler.serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt                             # 토큰 발행에 사용
from django.views.decorators.csrf import csrf_exempt
import json

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'POST':
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

@csrf_exempt
def hire_board(request):                    #받을 때 field 값은 그냥 plz에서 꺼내오는 걸로 해야함
    if request.method =='POST':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists(): 
            data = json.loads(request.body)
            user_class = Plz_class.objects.filter(plz_id = user_id)
            user_class_count = Plz_class.objects.filter(plz_id = user_id).count()
            u_class = ''
            for i in range(user_class_count):
                u_class = u_class + user_class[i] + ' '
            Hire_board.objects.create(
                plz_user = Plz.objects.filter(plz_id = user_id)
                plz_class = u_class
                title = data['title'],
                recruit = data['recruit'],
                need_member = data['need_member'],
                start_date = data['start_date'],
                end_date = data['end_date'],
                content = data['content'],
                apply_member = 0,
                data = timezone.datetime.now(),
            )
            return HttpResponse(status=200)
        else: return HttpResponse(status=401)
    else: return HttpResponse(status=401)

def apply(request):
    if request.method() == 'POST':
        user_id = tokenCheck(request)
        if Plus.objects.filter(plus_id = user_id).exists():
            data = json.loads(request.body)
            user_class = Plus_class.objects.filter(plus_id = user_id)
            u_class = ''
            for i in range(user_class.count()):
                u_class = u_class + user_class[i] + ' '
            board_number = data[number]
            plz_u = Hire_board.objects.filter(id = board_number)[0].plz_user #아니면 plz_id로
            Plus_apply.objects.create(
                plz_user = Plz.objects.filter(plz_id = plz_u),
                plus_user = Plus.objects.filter(plus_id = user_id),
                plus_class = u_class,
                plus_date = Plus_date.objects.filter(plus_id = user_id)[0].plus_start_day,
            )
            apply_number = Plus_apply.objects.filter(plz_id = plz_u).count()
            Hire_board.objects.filter(id = board_number).update(
                apply_member = apply_number 
            )
            return HttpResponse(status=200)
        else: return HttpResponse(status =401)
    else: return HttpResponse(status=400)

class Hire_board_listView(viewsets.ModelViewSet):
    queryset = Hire_board.objects.all()
    serializer_class = Hire_boardSerializer

def Hire_board_detail(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        b_number = data[number]
        board_title = Hire_board.objects.filter(id = b_number)[0].title
        board_content = Hire_board.objects.filter(id = b_number)[0].content
        board_recruit = Hire_board.objects.filter(id = b_number)[0].recruit
        board_need_member = Hire_board.objects.filter(id = b_number)[0].need_member
        board_start_date = Hire_board.objects.filter(id = b_number)[0].start_date
        board_end_date = Hire_board.objects.filter(id = b_number)[0].end_date
        board_apply = Hire_board.objects.filter(id = b_number)[0].apply_member
        plz_u = Hire_board.objects.filter(id = board_number)[0].plz_user #plz_id
        plz_user = Plz.objects.filter(plz_id = plz_u)[0]
        user_name = plz_user.plz_name
        user_class = Plz_class.objects.filter(plz_id = plz_u)
        u_class = ''
        for i in range(user_class.count()):
            u_class = u_class + user_class[i] + ' '
        return JsonResponse({"title" : board_title, "content" : board_content, "recruit" : board_recruit, "need_member" : board_need_member, "start_date" : board_start_date, "end_date" : board_end_date, "apply_member" : board_apply, "user_id" : plz_u, "user_name" : user_name, "user_field" : user_class}, status=200)
    else: return HttpResponse(status=400)
