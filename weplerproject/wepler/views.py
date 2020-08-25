from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Plus, Plz, Plus_class, Plus_day
from .form import PlusForm, PlzForm
import json
import bcrypt                            # 암호화에 사용
import jwt                             # 토큰 발행에 사용

def home(request):
    plus_user = Plus.objects
    plz_user = Plz.objects
    return render(request, 'home.html', {'plz_user': plz_user, 'plus_user' : plus_user})

def plus_signup(request):
    if request.method =='POST':
        name = request.POST['username']
        user_id = request.POST['id']
        password = request.POST['password1'].encode('utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
        address = request.POST['address']
        user_job = request.POST.get('job_check', '')

        user_class = request.POST.getlist('class_check', '')
        user_day = request.POST.getlist('day_check', '')

        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩

        p_user = Plus.objects.create(
            plus_id = user_id,
            plus_name = name,
            plus_password = password_crypt,
            plus_address = address,
            plus_job = user_job,
            plus_edu = False,
            plus_has_team= False,
        )

        for i in range(len(user_class)):
            Plus_class(
                plus_user = p_user,
                class_name = user_class[i],
            ).save()
        
        for j in range(len(user_day)):
            Plus_day(
                plus_user = p_user,
                day = user_day[j],
            ).save()
            
        return HttpResponse(status=200)
    else:
        return render(request, 'plus_signup.html')

def plz_signup(request):
    if request.method =='POST':
        name = request.POST['username']
        user_id = request.POST['id']
        password = request.POST['password1'].encode('utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
        address = request.POST['address']
        user_class = request.POST.getlist('class_check', '')
        if request.POST.get('group_check', '') == 'on':
            user_group = True
        else:
            user_group = False        

        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩

        p_user = Plz.objects.create(
            plz_id = user_id,
            plz_name = name,
            plz_password = password_crypt,
            plz_address = address,
            plz_group = user_group,
        )

        for i in range(len(user_class)):
            Plz_class(
                plz_user = p_user,
                class_name = user_class[i],
            ).save()
            
        return HttpResponse(status=200)
    else:
        return render(request, 'plz_signup.html')

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
