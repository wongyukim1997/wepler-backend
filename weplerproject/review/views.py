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
import json
from datetime import datetime, date

#review 작성할 때 완료된 리스트는 mypage에서 가져온다.

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'POST':
        token = request.headers.get('Authorization', None)
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

@csrf_exempt
def plus_review_detail(request, review_id):
    if request.method == 'GET':
        review = Plus_review.objects.filter(id = review_id)[0]
        review_title = review.title
        review_content = review.content
        review_Write = review.plz_user_id
        review_Write_name = review.plz_name
        review_plus = review.plus_user_id
        review_plus_name = review.plus_name
        review_point = review.plus_point
        review_plz_class = review.plus_class
        return JsonResponse({"writer" : review_Write, "writer_name" : review_Write_name, "matching" : review_plus, "matching_name" : review_plus_name, "writer_class" : review_plz_class, "title" : review_title, "content" : review_content, "rating" : review_point}, status=200)
    else: return HttpResponse(status=400)

@csrf_exempt
def plz_review_detail(request, review_id):
    if request.method == 'GET':
        review = Plz_review.objects.filter(id = review_id)[0]
        review_title = review.title
        review_content = review.content
        review_Write = review.plus_user_id
        review_Write_name = review.plus_name
        review_plz = review.plz_user_id
        review_plz_name = review.plz_name
        review_plus_class = review.plz_class
        return JsonResponse({"writer" : review_Write, "writer_name" : review_Write_name, "matching" : review_plz, "matching_name" : review_plz_name, "writer_class" : review_plus_class, "title" : review_title, "content" : review_content}, status =200)
    else: return HttpResponse(status=400)

def plus_review_count(request):
    if request.method == 'GET':
        count = Plus_review.objects.all().count()
        return JsonResponse({"count" : count}, status=200)
    else: return HttpResponse(status=400)

def plz_review_count(request):
    if request.method == 'GET':
        count = Plz_review.objects.all().count()
        return JsonResponse({"count" : count}, status=200)
    else: return HttpResponse(status=400)

@csrf_exempt
def plz_review_delete(request, review_id):
    if request.method == 'DELETE':
        review = Plz_review.objects.get(id = review_id)
        review.delete()
        return HttpResponse(status = 200)
    else: return HttpResponse(status=400)

@csrf_exempt
def plus_review_delete(request, review_id):
    if request.method == 'DELETE':
        review = Plus_review.objects.get(id = review_id)
        review.delete()
        return HttpResponse(status = 200)
    else: return HttpResponse(status=400)

#plz를 리뷰한 리스트
class Plz_review_list(viewsets.ModelViewSet):
    queryset = Plz_review.objects.all().order_by('-id')
    serializer_class = Plz_reviewSerializer

#plus를 리뷰한 리스트
class Plus_review_list(viewsets.ModelViewSet):
    queryset = Plus_review.objects.all().order_by('-id')
    serializer_class = Plus_reviewSerializer

@csrf_exempt
def review_update(request, review_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            review = Plus_review.objects.filter(id = review_id)[0]
            review.title = data['title']
            review.content = data['content']
            review.save()
            return HttpResponse(status=200)
        elif Plus.objects.filter(plus_id = user_id).exists():
            review = Plz_review.objects.filter(id = review_id)[0]
            review.title = data['title']
            review.content = data['content']
            review.save()
            return HttpResponse(status=200)
        else: return HttpResponse(status=400)
    else: return HttpResponse(status=400)

@csrf_exempt
def review_post(request):              #plus를 리뷰하는 함수(plz가 작성함)
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = tokenCheck(request)
        print(datetime.strptime(str(datetime.now().date()), '%Y-%m-%d'))
        if Plz.objects.filter(plz_id = user_id).exists():   #plz가 작성한다면
            if Match.objects.filter(plz_user_id=user_id).filter(complete=True).filter(plus_user_id=data['matchingEmail']).exists():
                if Plus_review.objects.filter(match_id=data['matching']).exists():
                    return JsonResponse({"hasuser" : True, "isoverap" : True}, status=200)
                else:
                    Plus_review.objects.create(
                        plus_user = Plus.objects.filter(plus_id = data['matchingEmail'])[0],
                        plz_user = Plz.objects.filter(plz_id = user_id)[0],
                        date = datetime.today().strftime('%Y-%m-%d'),
                        title = data['title'],
                        content = data['content'],
                        plus_name = Plus.objects.filter(plus_id = data['matchingEmail'])[0].plus_name,
                        plz_name = Plz.objects.filter(plz_id = user_id)[0].plz_name,
                        plus_point = data['rating'],
                        plus_class = Hire_board.objects.filter(plz_user = user_id)[0].plz_class,
                        match_id = data['matching'],
                    )
                    sum = 0
                    p_review = Plus_review.objects.filter(plus_user=data['matchingEmail'])
                    p_user = Plus.objects.filter(plus_id=data['matchingEmail'])[0]
                    p_user2 = Choice_board.objects.filter(plus_user=data['matchingEmail'])[0]
                    z_u = Plz_apply.objects.filter(plus_user=data['matchingEmail'])
                    s_u = Plus_apply.objects.filter(plus_user=data['matchingEmail'])
                    for i in range(p_review.count()):
                        sum = sum + p_review[i].plus_point
                    point = sum / p_review.count()
                    for i in range(z_u.count()):
                        z_user = Plz_apply.objects.filter(plus_user=data['matchingEmail'])[i]
                        z_user.plus_point=round(point, 1)
                        z_user.save()
                    for j in range(s_u.count()):
                        s_user = Plus_apply.objects.filter(plus_user=data['matchingEmail'])[i]
                        s_user.plus_point=round(point, 1)
                        s_user.save()
                    p_user.plus_point = round(point, 1)
                    p_user2.plus_point = round(point, 1)
                    p_user.save()
                    p_user2.save()
                    return JsonResponse({"hasuser" : True, "isoverap" : False}, status=200)
            else: return JsonResponse({"hasuser" : False}, status=200)
        elif Plus.objects.filter(plus_id = user_id).exists():   #plz가 작성한다면
            if Match.objects.filter(complete=True).filter(plz_user=data['matchingEmail']).exists():
                if Plz_review.objects.filter(match_id=data['matching']).exists():
                    return JsonResponse({"hasuser" : True, "isoverap" : True}, status=200)
                else:
                    Plz_review.objects.create(
                        plus_user = Plus.objects.filter(plus_id = user_id)[0],
                        plz_user = Plz.objects.filter(plz_id = data['matchingEmail'])[0],
                        date = datetime.today().strftime('%Y-%m-%d'),
                        title = data['title'],
                        content = data['content'],
                        plus_name = Plus.objects.filter(plus_id = user_id)[0].plus_name,
                        plz_name = Plz.objects.filter(plz_id = data['matchingEmail'])[0].plz_name,
                        plz_class = Plz.objects.filter(plz_id = data['matchingEmail'])[0].plz_class,
                        match_id = data['matching'],
                        )
                    return JsonResponse({"hasuser" : True, "isoverap" : False}, status=200)
            else: return JsonResponse({"hasuser" : False}, status=200)
        else: return HttpResponse(status=400)
    else: return HttpResponse(status=400)
