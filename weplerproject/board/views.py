from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from wepler.models import *
from wepler.serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt                                      # 토큰 발행에 사용
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
import json

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'POST':
        token = request.headers.get('Authorization', None)
        user_token_info = jwt.decode(token, SECRET_KEY, algorithm = "HS256")
        if Plus.objects.filter(plus_id=user_token_info['user_id']).exists() : #플리즈일 경우 'plus_id'가 key 에러로 걸린다.
            user_id = user_token_info['user_id']
            return user_id
        elif Plz.objects.filter(plz_id=user_token_info['user_id']).exists() :
            user_id = user_token_info['user_id']
            return user_id 
        return HttpResponse(status=403)
    else:
        HttpResponse(status=400)

@csrf_exempt
def hire_board(request):                    # 받을 때 field 값은 그냥 plz에서 꺼내오는 걸로 해야함
    if request.method =='POST':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists(): 
            data = json.loads(request.body)
            user_class = Plz_class.objects.filter(plz_user = user_id)
            u_class = ''
            is_timeover = "모집중"
            a = datetime.strptime(str(data['recruit']), '%Y-%m-%d')      #정한 시간
            b = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')      #지금 시간, 정한 시간보다 작아야함
            if a < b :
                is_timeover = "모집 마감"
            for i in range(user_class.count()):
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
            Hire_board.objects.create(
                plz_user = Plz.objects.filter(plz_id = user_id)[0], 
                plz_class = u_class,
                title = data['title'],
                recruit = data['recruit'],
                need_member = data['need_member'],
                start_date = data['start_date'],
                end_date = data['end_date'],
                content = data['content'],
                apply_member = 0,
                date = timezone.datetime.now(),
                timeover = is_timeover,
                plz_group = Plz.objects.filter(plz_id = user_id)[0].plz_group,
            )
            return HttpResponse(status=200)
        else: return HttpResponse(status=401)
    else: return HttpResponse(status=401)

def list_count(request):
    if request.method == 'GET':
        h_count = Hire_board.objects.all().count()
        return JsonResponse({"count" : h_count}, status=200)
    else: return HttpResponse(status=400)

@csrf_exempt
def apply(request, board_id):
    if request.method == 'POST':
        user_id = tokenCheck(request)
        if Plus.objects.filter(plus_id = user_id).exists():
            user_class = Plus_class.objects.filter(plus_user = user_id)
            u_class = ''
            for i in range(user_class.count()):
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
            user_day = Plus_date.objects.filter(plus_user = user_id)
            u_day = ''
            for j in range(user_day.count()):
                u_day = u_day + user_day[j].plus_start_day + ' '
            plz_u = Hire_board.objects.filter(id = board_id)[0].plz_user_id
            a = datetime.strptime(str(Hire_board.objects.filter(id=board_id)[0].recruit), '%Y-%m-%d')      #정한 시간
            b = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
            
            if a < b:
                return JsonResponse({"istimeover" : True}, status=200)
            elif Plus_apply.objects.filter(hire_id=board_id).filter(plus_user=user_id).exists():
                return JsonResponse({"isoverap" : True}, status=200)
            else:
                Plus_apply.objects.create(
                    plz_user = Plz.objects.filter(plz_id = plz_u)[0],
                    plus_user = Plus.objects.filter(plus_id = user_id)[0],
                    plus_user_name = Plus.objects.filter(plus_id = user_id)[0].plus_name,
                    plus_address = Plus.objects.filter(plus_id = user_id)[0].plus_address_big,
                    title = Hire_board.objects.filter(plz_user = plz_u)[0].title,
                    plz_class = Hire_board.objects.filter(id=board_id)[0].plz_class,
                    plus_date = u_day,
                    hire_id = Hire_board.objects.filter(id=board_id)[0],
                    plus_point = Plus.objects.filter(plus_id = user_id)[0].plus_point,
                    plus_class = u_class,
                )
                apply_number = Plus_apply.objects.filter(plz_user = plz_u).count()
                h_board = Hire_board.objects.filter(id = board_id)[0]
                h_board.apply_member = apply_number
                h_board.save()
                return JsonResponse({"isoverap" : False}, status=200)
        else: return HttpResponse(status =401)
    else: return HttpResponse(status=400)

class Hire_board_listView(viewsets.ModelViewSet):
    queryset = Hire_board.objects.all().order_by('-id')
    serializer_class = Hire_boardSerializer

@csrf_exempt
def hire_delete(request, board_id):
    if request.method == 'DELETE':
        h_board = Hire_board.objects.get(id = board_id)
        h_board.delete()
        return HttpResponse(status = 200)
    else: return HttpResponse(status=400)

@csrf_exempt
def hire_update(request, board_id):
    print("작동")
    if request.method == 'POST':
        data = json.loads(request.body)
        h_board = Hire_board.objects.get(id = board_id)
        h_board.title = data['title']
        h_board.content = data['content']
        h_board.start_date = data['start_date']
        h_board.end_date = data['end_date']
        h_board.need_member = data['need_member']
        h_board.save()
        return HttpResponse(status = 200)
    return HttpResponse(status=400)

def Hire_board_detail(request, board_id):
    if request.method == 'GET':
        read_id = tokenCheck(request)
        print(board_id)
        h_board = Hire_board.objects.filter(id = board_id)[0]
        board_title = h_board.title
        board_content = h_board.content
        board_recruit = h_board.recruit
        board_need_member = h_board.need_member
        board_start_date = h_board.start_date
        board_end_date = h_board.end_date
        board_apply = h_board.apply_member
        plz_u = h_board.plz_user_id                                   
        plz_user = Plz.objects.filter(plz_id = plz_u)[0]
        user_name = plz_user.plz_name
        user_group = plz_user.plz_group
        user_class = h_board.plz_class
        return JsonResponse({"read_id" : read_id, "title" : board_title, "content" : board_content, "recruit" : board_recruit, "need_member" : board_need_member, "start_date" : board_start_date, "end_date" : board_end_date, "apply_member" : board_apply, "user_id" : plz_u, "user_name" : user_name, "user_field" : user_class, "user_belong" : user_group}, status=200)
    else: return HttpResponse(status=400)


