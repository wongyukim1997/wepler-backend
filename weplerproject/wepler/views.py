from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import bcrypt                            # 암호화에 사용
import jwt                             # 토큰 발행에 사용

class Plus_signupView(APIView):
    def post(self, request):
        serializer = PlusSerializer(data = request.data)
        if serializer.is_valid():
            password = serializer.data['plus_password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
            Plus.objects.create(
                plus_id= serializer.data['plus_id'],
                plus_name= serializer.data['plus_name'],
                plus_password = password_crypt,
                plus_address = serializer.data['plus_address'],
                plus_edu = False;
                Plus_has_team =False;
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class Plz_signupView(APIView):
    def post(self, request):
        serializer = PlzSerializer(data = request.data)
        if serializer.is_valid():
            password = serializer.data['plus_password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
            Plz.objects.create(
                plz_id= serializer.data['plus_id'],
                plz_name= serializer.data['plus_name'],
                plz_password = password_crypt,
                plz_address = serializer.data['plus_address'],
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def plus_login(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method =='POST':
        user_id = request.POST['id']
        password = request.POST['password1'].encode('utf-8')   
        if Plus.objects.filter(plus_id = user_id).exists():
            user = Plus.objects.get(plus_id = user_id)          #입력된 id가 존재하면, 그 id를 가진 plus를 user라는 변수에 넣었음
            if bcrypt.checkpw(request.POST['password1'].encode('utf-8'), user.plus_password.encode('utf-8')) :          #입력된 비밀번호와 변수 user(입력된 id를 가진 plus)의 비밀번호를 비교
                token = jwt.encode({'plus_id' : user.plus_id}, SECRET_KEY, algorithm = "HS256")
                token = token.decode('utf-8')                                                                           # 유니코드 문자열로 디코딩
                return JsonResponse({"token" : token }, status=200)
            else:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=400)
    else:
        return render(request, 'plus_login.html')

def plz_login(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method =='POST':
        user_id = request.POST['id']
        password = request.POST['password1'].encode('utf-8')   
        if Plz.objects.filter(plz_id = user_id).exists():
            user = Plz.objects.get(plz_id = user_id)          #입력된 id가 존재하면, 그 id를 가진 plz를 user라는 변수에 넣었음
            if bcrypt.checkpw(request.POST['password1'].encode('utf-8'), user.plz_password.encode('utf-8')) :          #입력된 비밀번호와 변수 user(입력된 id를 가진 plz)의 비밀번호를 비교
                token = jwt.encode({'plz_id' : user.plz_id}, SECRET_KEY, algorithm = "HS256")
                token = token.decode('utf-8')                                                                           # 유니코드 문자열로 디코딩
                return JsonResponse({"token" : token }, status=200)
            else:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=400)
    else:
        return render(request, 'plz_login.html')
